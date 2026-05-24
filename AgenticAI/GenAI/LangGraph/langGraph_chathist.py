from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages

from langchain_groq import ChatGroq

llm=ChatGroq(model="openai/gpt-oss-120b")

class State(TypedDict):
    messages: Annotated[list,add_messages]


def chatbot(state:State):
    response=llm.invoke(state["messages"])
    state["messages"]=response
    return state

def sample_node(state:State):
    print("Inside Sample Node",state)
    state["messages"]=["Sample node message"]
    return state

graph_builder=StateGraph(State)
graph_builder.add_node("chatbot_node",chatbot)
graph_builder.add_node("sample_node",sample_node)
graph_builder.add_edge(START,"chatbot_node")
graph_builder.add_edge("chatbot_node","sample_node")
graph_builder.add_edge("sample_node",END)

graph=graph_builder.compile()

print(graph.get_graph().draw_ascii())

response=graph.invoke(State({"messages":["What is my name"]}))
print("Finale State\n",response)