from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
#Checkpoint
from langgraph.checkpoint.mongodb import MongoDBSaver

llm=ChatGroq(model="openai/gpt-oss-120b")

class State(TypedDict):
    messages: Annotated[list,add_messages]


def chatbot(state:State):
    response=llm.invoke(state["messages"])
    state["messages"]=response
    return state


graph_builder=StateGraph(State)
graph_builder.add_node("chatbot_node",chatbot)

graph_builder.add_edge(START,"chatbot_node")
graph_builder.add_edge("chatbot_node",END)

graph=graph_builder.compile()

print(graph.get_graph().draw_ascii())

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

##Provinding the Checkpoint to store the messsages
DB_URI="mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer=compile_graph_with_checkpointer(checkpointer)

    config={
        "configurable":{
            "thread_id":"nithya_sai"
        }
    }
    response=graph_with_checkpointer.invoke(State({"messages":["I like green tea"]}),config=config)
    print(response)
    # for chunk in graph_with_checkpointer.stream(State({"messages":["What is my name?"]}),config,stream_mode="values"):
    #     chunk["messages"][-1].pretty_print()




# response=graph.invoke(State({"messages":["What is my name"]}))
# print("Finale State\n",response)