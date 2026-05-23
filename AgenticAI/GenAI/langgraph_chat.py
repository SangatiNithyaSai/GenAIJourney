from dotenv import load_dotenv
load_dotenv()

from typing import Optional,Literal

from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from google import genai

from langchain_groq import ChatGroq
client=genai.Client()
llm=ChatGroq(model="openai/gpt-oss-120b")

class State(TypedDict):
    user_query:str
    llm_output: Optional[str]
    is_good:Optional[bool]

def chatbot(state:State):
    print("Chatbot node",state)
    response=client.models.generate_content(model="gemini-2.5-flash",
                                            contents=[state.get("user_query")])
    state["llm_output"]=response.candidates[0].content
    return state


graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State(user_query="What all tools are you connected to?"))
print(updated_state)


