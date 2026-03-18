import os
from dotenv import load_dotenv
import streamlit as st
# loading the llm model
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


#langchan tracking
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']=os.getenv("LANGSMITH_PROJECT")


#Prompt Template
promt=ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpul assistant, please respond to questions asked"),
        ("user","Question:{question}")
    ]

)

#strealit framework
st.title("Langchain Demo with ollama Gemma Model")
input_text=st.text_input("Question????????")
#LLm model
llm=Ollama(model="llama3.2:3b")
chain=promt|llm|StrOutputParser()
try:
    if input_text:
        response=chain.invoke({
        "question":input_text})
        st.write(response)
    else:
        st.write("Ask the question")
except Exception as e:
    st.write(f"Exeception is {e}")