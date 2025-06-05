# utils/retriever.py

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

def create_retriever_from_kb(kb_path):
    # Read knowledge base facts
    with open(kb_path, 'r') as f:
        kb_data = f.read().splitlines()

    docs = [Document(page_content=fact) for fact in kb_data if fact.strip()]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever
