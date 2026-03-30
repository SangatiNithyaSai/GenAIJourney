import streamlit as st
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm=ChatGroq(model="llama-3.3-70b-versatile")

prompt=ChatPromptTemplate.from_template(
""" 
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.
Context:
{context}
Question:{input}
"""
)

#create vector to store in the session
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings=embeddings
        st.session_state.loader=PyPDFDirectoryLoader('research_papers')
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents=st.session_state.splitter.split_documents(st.session_state.docs[:50])
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

##UI
st.title("RAG Documnet Q&A with Groq and HuggingFace API's")

user_prompt=st.text_input("Enter your query related to LLMS and Attention Mechanism")

if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Vector Database is ready")

import time

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain


if user_prompt:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)

    start=time.process_time()
    response=retrieval_chain.invoke({'input':user_prompt})
    print(f'Response Time:{time.process_time()-start}')
    st.write(response['answer'])
    
    #To see the retreived context
    with st.expander("Documnet Similarity search"):
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write('---------------------')




