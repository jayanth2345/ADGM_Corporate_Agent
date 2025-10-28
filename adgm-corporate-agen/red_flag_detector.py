# red_flag_detector.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Use local Llama 3 model (free)
llm = ChatOllama(model="llama3", temperature=0.2)

prompt = ChatPromptTemplate.from_template("""
You are an ADGM legal compliance expert.
Review the document and identify issues using ONLY the context below.

Context from ADGM Rules:
{context}

Document Type: {doc_type}
Content: {content}

Identify red flags such as:
- Wrong jurisdiction (e.g., UAE/Dubai Courts instead of ADGM)
- Missing clauses
- Ambiguous language
- Non-compliance with templates

Return a JSON list with:
- section (e.g., Clause 3.1)
- issue (description)
- severity (High/Medium/Low)
- suggestion (corrective action)

Only use context. Do NOT invent rules.
""")

def detect_red_flags(content: str, doc_type: str, retriever) -> list:
    try:
        relevant_docs = retriever.invoke(content[:2000])
        context = "\n".join([d.page_content for d in relevant_docs])

        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({
            "context": context,
            "doc_type": doc_type,
            "content": content[:2000]
        })
        return result
    except Exception as e:
        print(f"Error in LLM: {e}")
        return []