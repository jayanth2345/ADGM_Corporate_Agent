
DOCUMENT_KEYWORDS = {
    "Articles of Association": ["articles", "association", "aoa", "shareholder rights"],
    "Memorandum of Association": ["memorandum", "moa", "objects clause"],
    "UBO Declaration": ["ultimate beneficial owner", "ubo", "ownership structure"],
    "Register of Members and Directors": ["register", "members", "directors", "appointment"],
    "Incorporation Application Form": ["application for incorporation", "aca1", "form aca"],
    "Board Resolution": ["board resolution", "resolved that", "directors meeting"],
    "Shareholder Resolution": ["shareholder resolution", "ordinary resolution"]
}

def detect_document_type(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for doc_name, keywords in DOCUMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[doc_name] = score
    return max(scores, key=scores.get) if scores else "Unknown"

REQUIRED_DOCS = [
    "Articles of Association",
    "Memorandum of Association",
    "UBO Declaration",
    "Register of Members and Directors",
    "Incorporation Application Form"
]

def check_missing_documents(uploaded_types):
    uploaded_set = set(uploaded_types)
    missing = [doc for doc in REQUIRED_DOCS if doc not in uploaded_set]
    return missing