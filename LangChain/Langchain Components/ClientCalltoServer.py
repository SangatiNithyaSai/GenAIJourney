import requests
import streamlit as st

def get_groq_response(input_text,language):
    json_body={
        "input": {
        "text": input_text,
        "language": language
        },
        "config": {},
        "kwargs": {
        "additionalProp1": {}
        }
     }
    response=requests.post("http://127.0.0.1:8000/chain/invoke",json=json_body) ##use json= so that the url uses the data as json
    return response.json()
    
st.title(" Language Translation using Groq by APIs")
input_text=st.text_input("Enter the sentence to translate")
language=st.text_input("Enter the language in which the sentence to be translated")
if input_text and language:
    with st.spinner("Getting response"):
        st.write(get_groq_response(input_text=input_text,language=language)['output'])
else:
    st.write("Give both Input text and language")