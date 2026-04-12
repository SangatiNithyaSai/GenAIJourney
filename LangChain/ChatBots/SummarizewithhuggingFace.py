import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEndpoint

#Streamlit App
st.set_page_config(page_title="Langchain:Summarize Text from YT or WebURL",page_icon="🦜")
st.title("🦜 Summarize Text from YT or Website")
st.subheader('Summarize URl')

#get HF token
with st.sidebar:
    hf_api_key=st.text_input("Hugging Face API Token",value="",type="password")

generic_url=st.text_input("URL",label_visibility="collapsed")

repo_id="meta-llama/Meta-Llama-3-8B"
llm=HuggingFaceEndpoint(repo_id=repo_id,temperature=0.8,huggingfacehub_api_token=hf_api_key,task="text-generation")

prompt_template=""" 
Provide a summary of the following content in 300 words
Text:{text}
"""
prompt=PromptTemplate(input_variables=['text'],template=prompt_template)

if st.button("Summarize content from YT or website"):
    #Input validation
    if not hf_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("please enter a valid URL")
    
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                    print("hi")
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                print("hi2")
                docs=loader.load()
                print("hi3")
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)     
                print("hi4")
                output_summary=chain.run(docs)  
                st.success(output_summary)                                 

        except Exception as e:
            st.exception(f"Error is :{e}")
            


