import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.prompts import PromptTemplate
from langchain_classic.callbacks import StreamlitCallbackHandler

from langchain.agents import create_agent
from langchain_classic.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.chains.llm_math.base import LLMMathChain

st.set_page_config(page_title="Text to Math problem Solver and Data Search assistant",page_icon="🧮")
st.title("Text to math problem solver using Google gemma 2")

groq_api_key=st.text_input("Provide Groq API key",type="password")

if not groq_api_key:
    st.info("Please add your Groq API key")
    st.stop()

llm=ChatGroq(model="Gemma2-9b-It",api_key=groq_api_key)

#iniializing the tools

wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet to find the various information on the topics mentioned"   
)

#calculator tool
math_chain=LLMMathChain.from_llm(llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering with relvant questions.Only input mathematical expression need to be provided"
)

prompt=""" 
You are an agent ,tasked for solving user mathematical question.Logically arrive at a solution and provide 
detailed explaination point wise for the question below:
question:{question}
"""

prompt_template=PromptTemplate(input_variables=['question'],template=prompt)

chain=prompt_template | llm

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.invoke,
    description="A tool for answering logic-based and reasoning question"
)

assistant_agent=create_react_agent(llm,tools=[wikipedia_tool,reasoning_tool,calculator])

''' 
input_question=st.text_input("Enter any logival or mathematical question")

if input_question:
    response=assistant_agent.invoke({"messages":[{"role":"user","content":input_question}]})
    st.write(response)
'''

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

question=st.text_area("Enter your question","I have 5 apples ,2 bananas , 1 orange. I gave 2 bananas to my friend. He gave me two boxes of grapes each box having 4 grapes. How many fruits do I have finally?")
if st.button("find my answer"):
    if question:
        with st.spinner("Generate response .."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.invoke(st.session_state.messages,config={"callbacks":[st_cb]})
            st.write("### Response")
            st.success(response)
    else:
        st.warning("Ask the question")

