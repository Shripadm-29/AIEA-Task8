# utils/retriever.py

# Import FAISS (a vector database for storing and searching embeddings)
from langchain_community.vectorstores import FAISS

# Import OpenAI embeddings (turns text into vectors/numbers so we can search)
from langchain_openai import OpenAIEmbeddings

# Import Document (LangChain's way of wrapping a piece of text)
from langchain_core.documents import Document

def create_retriever_from_kb(kb_path):
    # Step 1: Read knowledge base file line by line
    with open(kb_path, 'r') as f:
        kb_data = f.read().splitlines()

    # Step 2: Wrap each fact into a Document object
    # (only keep non-empty lines)
    docs = [Document(page_content=fact) for fact in kb_data if fact.strip()]

    # Step 3: Create embeddings (numbers) for each fact using OpenAI
    embeddings = OpenAIEmbeddings()

    # Step 4: Store the documents + embeddings inside a FAISS vector database
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Step 5: Turn the vectorstore into a retriever
    # - search_type="similarity": find the most similar facts
    # - k=5: return the top 5 closest matches
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Step 6: Return the retriever so we can use it in other files
    return retriever
