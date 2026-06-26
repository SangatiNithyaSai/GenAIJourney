from dotenv import load_dotenv

from pathlib import Path 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from google.genai import Client,types
import os


load_dotenv()



client=Client(api_key=os.getenv('GOOGLE_API_KEY'))

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
pdf_path=Path(__file__).parent / "Python Programming.pdf"

#Load the file in python program

loader= PyPDFLoader(file_path=pdf_path)
docs=loader.load()

#Split the docs into smaller chunks

text_spiltter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks=text_spiltter.split_documents(documents=docs)
#vector Embeddings


vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing of documents done...")