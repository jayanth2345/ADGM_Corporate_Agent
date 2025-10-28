# rag_loader.py
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Use free local embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_adgm_knowledge(base_path="templates/reference_adgm_docs"):
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Folder not found: {os.path.abspath(base_path)}")

    loader = DirectoryLoader(base_path, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore.as_retriever()