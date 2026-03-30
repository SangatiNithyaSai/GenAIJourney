import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
prompt=ChatPromptTemplate.from_messages(
    {
        ("system","You are an helpful assistant, Answer as good as possible"),
        ("user","{question}")
    }
)

def generate_response(model_name,api_key,temperature,max_tokens,question):
    llm=ChatGroq(model=model_name,api_key=api_key,temperature=temperature,max_tokens=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    response= chain.invoke({"question":question})
    return response


##Streamlit UI starts from here

st.title("Enhanced Chatbot with Ollama Models")
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter the api Key",type="password")
temp=st.sidebar.slider("Choose the temperature",min_value=0.0,max_value=1.0,value=0.4)
max_tokens=st.sidebar.slider("Choose the tokens size",min_value=125,max_value=500,value=250)
model=st.sidebar.selectbox("Choose the model",["meta-llama/llama-4-scout-17b-16e-instruct","llama-3.3-70b-versatile"])

st.write("Go Ahead and ask any question")
question=st.text_input("Enter any question")

if question and api_key:
    response=generate_response(model,api_key,temp,max_tokens,question)
    st.write(response)
elif question:
    st.warning("Provide the api _key")
else:
    st.warning("Ask the question")

