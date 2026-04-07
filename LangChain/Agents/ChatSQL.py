import streamlit as st
from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks import StreamlitCallbackHandler
#from langchain.agents import create_agent
from langchain.agents import create_agent
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from streamlit.runtime.scriptrunner import get_script_run_ctx
st.set_page_config(page_title="Langchain:Chat with SQL DB",page_icon="🦜")
st.title("🦜Langchain :Chat with SQL")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLlite3 Database -student.db","Use your own existing DB"]

selected_opt=st.sidebar.radio(label="choose the DB you want to use",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MYSQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL Password",type="password")
    mysql_db=st.sidebar.text_input("Enter the Database name")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input("Enter the Groq API key",type="password")

if not db_uri:
    st.info("Please enter the database information")

if not api_key:
    st.info("Please provide the Groq API")

##LLM Model
llm=ChatGroq(api_key=api_key,model="openai/gpt-oss-120b",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator= lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==MYSQL:
        if not(mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("please Provide all MySQL connection details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)

##toolkit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)


system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=5,
)


tools=toolkit.get_tools()
agent=create_agent(
    model=llm,tools=tools,system_prompt=system_prompt
)
"""
agent=create_agent(
    model=llm,tools=toolkit,system_prompt=system_prompt
)
"""
# To check the working of the agent uncomment below
'''
question="give me names of the students"
print(agent.invoke({
    "messages":[{'role':'user','content':question}]
}))
'''

if "messages" not in st.session_state or st.sidebar.button("Clear messages"):
    st.session_state["messages"]=[{"role":"assistant","content":"How Can I help you?"}]

for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])
user_query=st.chat_input(placeholder="Ask any question from the Database")

if user_query:
    st.session_state.messages.append({'role':'user','content':user_query})
    st.chat_message('user').write(user_query)
    ctx = get_script_run_ctx()
    with st.chat_message('assistant'):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        streamlit_callback.run_context=ctx
        response=agent.invoke({ "role":"user","content":user_query},
                              config={"callbacks":[streamlit_callback]})
        st.session_state.messages.append({'role':'assistant','content':response["messages"][-1].content})
        st.write(response["messages"][-1].content)
    print(st.session_state.messages)
    