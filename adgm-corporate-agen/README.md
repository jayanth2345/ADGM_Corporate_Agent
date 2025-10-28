# ADGM Corporate Agent

An AI-powered legal assistant that reviews, validates, and helps prepare documentation for company incorporation in the Abu Dhabi Global Market (ADGM).

# Features

- Upload `.docx` files
- Auto-detect document types (e.g., AoA, UBO Declaration)
- Check missing documents for ADGM incorporation
- Detect legal red flags using RAG + LLM
- Insert contextual comments into `.docx`
- Output reviewed `.docx` + structured JSON report
- Fully compliant with ADGM rules via RAG

# Functional Objectives (from Task)

✅ Accept `.docx` documents  
✅ Parse and identify document types  
✅ Check completeness against ADGM checklist  
✅ Detect red flags (jurisdiction, missing clauses)  
✅ Insert comments in `.docx`  
✅ Output downloadable reviewed file  
✅ Generate structured JSON report  
✅ Use RAG with ADGM rules for legal accuracy

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **LangChain** (RAG pipeline)
- **Ollama + Llama 3** (Free local LLM)
- **HuggingFaceEmbeddings** (`all-MiniLM-L6-v2`)
- **FAISS** (Vector storage)
- **python-docx** (Document editing)

> 🔐 No OpenAI API key required — runs 100% free and offline.

# Installation & Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/yourname/adgm-corporate-agent.git
   cd adgm-corporate-agent