from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
from dotenv import load_dotenv
from document_checker import detect_document_type, check_missing_documents
from rag_loader import load_adgm_knowledge
from red_flag_detector import detect_red_flags
from comment_injector import inject_comments
from docx import Document
import json

load_dotenv()

st.title("🛡️ ADGM Corporate Agent")
st.subheader("AI-Powered Legal Document Review for ADGM Compliance")

uploaded_files = st.file_uploader("Upload .docx files", type="docx", accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Loading ADGM knowledge base..."):
        retriever = load_adgm_knowledge()

    uploaded_types = []
    all_issues = []
    docs_with_type = {}

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs/reviewed", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)

    for file in uploaded_files:
        input_path = os.path.join("uploads", file.name)
        with open(input_path, "wb") as f:
            f.write(file.getbuffer())

        doc = Document(input_path)
        full_text = "\n".join([p.text for p in doc.paragraphs])
        doc_type = detect_document_type(full_text)
        uploaded_types.append(doc_type)
        docs_with_type[file.name] = doc_type

        st.write(f"📄 {file.name} → **{doc_type}**")

        issues = detect_red_flags(full_text, doc_type, retriever)
        for issue in issues:
            issue['document'] = file.name
        all_issues.extend(issues)

        output_path = os.path.join("outputs/reviewed", f"Reviewed_{file.name}")
        inject_comments(input_path, output_path, issues)

    process = "Company Incorporation" if "Articles of Association" in uploaded_types else "Unknown Process"
    missing_docs = check_missing_documents(uploaded_types)

    if missing_docs:
        st.warning(f"It appears you’re trying to incorporate a company in ADGM. You have uploaded {len(uploaded_files)} out of 5 required documents. Missing: **{', '.join(missing_docs)}**")

    report = {
        "process": process,
        "documents_uploaded": len(uploaded_files),
        "required_documents": 5,
        "missing_documents": missing_docs,
        "issues_found": all_issues
    }

    st.json(report)

    report_path = "outputs/reports/compliance_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    with open(report_path, "rb") as f:
        st.download_button("📥 Download JSON Report", f, file_name="compliance_report.json")

    for file in uploaded_files:
        reviewed_name = f"Reviewed_{file.name}"
        reviewed_path = os.path.join("outputs/reviewed", reviewed_name)
        with open(reviewed_path, "rb") as f:
            st.download_button(f"📄 Download {reviewed_name}", f, file_name=reviewed_name)