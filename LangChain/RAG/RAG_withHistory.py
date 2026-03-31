# RAG Q&A with pdf along with Chat history
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['HF_TOKEN']=os.getenv('HF_TOKEN')
import json
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
##run this if you are using ubuntu system and facing sqllite version issue
# --- STEP 1: THE FIX (MUST BE FIRST) ---
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# --- STEP 2: VERIFY ---
import sqlite3
print(f"Current SQLite version: {sqlite3.sqlite_version}")
from langchain_chroma.vectorstores import Chroma

#chat history to be saved
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever,create_retrieval_chain

#Prompts
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory


embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#setting up streamlit
st.title("Conversational RAG with PDF uploads and chat history ")
st.write("Upload Pdf and chat with there content")

#get api key
api_key=st.text_input("Enter your Groq API key:",type='password')

#check if api key is provided or not
if api_key:
    llm=ChatGroq(model_name="Gemma2-9b-It",api_key=api_key)
    #chat interface
    session_id=st.text_input("Session ID",value="default_session")
    #statefully manage chat history
    if 'store' not in st.session_state:
        st.session_state.store={}
    
    uploaded_files=st.file_uploader('Chosse a PDF File',type='pdf',accept_multiple_files=True)
    #Process uploaded PDF
    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            temppdf="./temp.pdf"
            with open(temppdf,'wb') as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
        ##Loading the documents
            loader=PyPDFLoader(temppdf)
            docs=loader.load()
            documents.extend(docs) 
        ##splitting and embedding
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=500)
        splits=text_splitter.split_documents(documents=documents)
        vectorstore=Chroma.from_documents(documents=splits,embedding=embedding)
        retriever=vectorstore.as_retriever()
        contextualize_que_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_que_prompt=ChatPromptTemplate.from_messages(
            [
                ("system",contextualize_que_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")

            ]
        )
        history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_que_prompt)

        

else:
    st.warning("Provide the API Key")
