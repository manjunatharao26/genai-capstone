from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Create embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

def create_vector_store(mission_text):
    # Split content
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(mission_text)]

    # Build vector DB
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore
