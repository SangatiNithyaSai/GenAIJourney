import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper,DuckDuckGoSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_classic.callbacks import StreamlitCallbackHandler
import os

from dotenv import load_dotenv
load_dotenv()

arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)

wiki_tool=WikipediaQueryRun(api_wrapper=wiki_wrapper,name="wiki_tool")
arxiv_tool=ArxivQueryRun(api_wrapper=arxiv_wrapper,name="arxiv_tool")

#search=DuckDuckGoSearchAPIWrapper()
#search_tool=DuckDuckGoSearchRun(api_wrapper=search,name="search")
st.title("Langchain- Chat with search")
api_key=st.sidebar.text_input("Enter your Groq API key",type="password")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi I am a chatbot,who can search the web.How can I help you?"}
    ]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:=st.chat_input(placeholder="What is machine learning"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    llm=ChatGroq(api_key=api_key,model="openai/gpt-oss-120b")
    tools=[arxiv_tool,wiki_tool] #,search_tool]

    search_agent=create_react_agent(llm,tools)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.invoke(st.session_state.messages,
                                     config={"callbacks": [st_cb]})
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)
        