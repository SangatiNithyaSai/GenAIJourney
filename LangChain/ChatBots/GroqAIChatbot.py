import streamlit as st
from  langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


##Prompt template
prompt=ChatPromptTemplate(
    {
        ("system","You are an helpful assistant, Please respond to user queries"),
        ("user","Question:{question}")
    }    
)

def generate_response(user_input,api_key,engine,temp,max_tokens):
    llm=ChatGroq(model=engine,temperature=temp,max_tokens=max_tokens,api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    ans=chain.invoke({'question':user_input})
    return ans

##Title of the app

st.title("Enhanced Q&A Chatbot with Groq")
#Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter the GroqAPI",type="password")

#select the model
engine=st.sidebar.selectbox("Select the Groq models",["openai/gpt-oss-120b","openai/gpt-oss-120b","qwen/qwen3-32b"])

#adjust the response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max_tokens",min_value=50,max_value=300,value=150)

#Main Interface for user

st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input and api_key:
    response=generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the api key")
else:
    st.warning("Please Provide the user input")