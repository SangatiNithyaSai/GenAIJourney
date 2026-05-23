from dotenv import load_dotenv
load_dotenv()
from rich import print
from typing import Optional,Literal

from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from google import genai

from langchain_groq import ChatGroq
client=genai.Client()
llm_chatgpt=ChatGroq(model="openai/gpt-oss-120b")
llm_evaluator=ChatGroq(model="qwen/qwen3-32b")

class State(TypedDict):
    user_query:str
    gemini_response:Optional[str]
    gpt_response:Optional[str]
    best_output: Optional[str]

def chatbot_gemini(state:State):
    print("\n Gemini Chatbot node: ",state)
    response=client.models.generate_content(model="gemini-2.5-flash",
                                            contents=[state.get("user_query")])
    state["gemini_response"]=response.candidates[0].content.parts[0].text
    return state
def chatbot_gpt(state:State):
    print("\n GPT chatbot:",state)
    response=llm_chatgpt.invoke(state["user_query"])
    state['gpt_response']=response.content
    return state

def evaluation_response(state:State):
    print("\nevaluate_response_node: ",state)
    
    # evaluation_prompt = f"""
    # You are an expert evaluator.

    # Compare the following two responses.

    # USER QUESTION:
    # {state['user_query']}

    # RESPONSE A (Gemini):
    # {state['gemini_response']}

    # RESPONSE B (GPT):
    # {state['gpt_response']}

    # Evaluate both responses on:
    # 1. Correctness
    # 2. Clarity
    # 3. Completeness
    # 4. Hallucination risk
    # 5. Conciseness
    # Identify the final winner and provide me a json file
    # {{
    # 'final_winner':'' #gemini_response or gpt_response
    # 'reason:''
    # }}. 
    # """
    evaluation_prompt = f"""
    You are an expert evaluator.

    Compare the following responses.

    USER QUESTION:
    {state['user_query']}

    RESPONSE A (Gemini):
    {state['gemini_response']}

    RESPONSE B (GPT):
    {state['gpt_response']}
    Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.
Do not include <think> tags.
    Return ONLY valid JSON in this format:
   
    {{
        "gemini_score": 0,
        "gpt_score": 0,
        "winner": "",
        "reason": ""
    }}
    """
    response=llm_evaluator.invoke(evaluation_prompt)
    state["best_output"]=response.content
    return state




graph_builder=StateGraph(State)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("chatbot_gpt",chatbot_gpt)
graph_builder.add_node("LLM_As_Judge",evaluation_response)

graph_builder.add_edge(START,"chatbot_gemini")
graph_builder.add_edge("chatbot_gemini","chatbot_gpt")
graph_builder.add_edge("chatbot_gpt","LLM_As_Judge")
graph_builder.add_edge("LLM_As_Judge",END)

graph=graph_builder.compile()

print(graph.get_graph().draw_ascii())
updated_state=graph.invoke(State(user_query="Answer the question in 50 words.What is Context manager in FastAPI?"))
print(updated_state)


