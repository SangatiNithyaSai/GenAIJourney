from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import Optional
from google import genai
from google.genai.types import GenerateContentConfig
load_dotenv()
import requests
import os
import json
from rich import print
client=genai.Client()

def run_command(cmd:str):
    result=os.system(cmd)
    return result


def get_weather(city:str):
    """ This function is used for retrieving the weather status of the provided city"""
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response= requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"



available_tools={
    "get_weather":get_weather,
    "run_command":run_command
}





SYSTEM_PROMPT= """ 
You are an expert in answering the user using Chain Of Thought.
you work on START,PLAN and OUTPUT Steps.
you need to first PLAN before doing a task. A plan can have many steps.
Once you think enough PLAN has be done,finally you can give an OUTPUT.

Rules:
- Strictly follow the given JSON Output format.
- Only run one step at a time.
- The sequence of steps is START(where user gives an input), PLAN(that can be multiple times) 
and finally OUTPUT(which is goining to be displayed to the user)

Output JSON Format:
{"step": "START"|"PLAN"|"OUTPUT"|"TOOL"|"OBSERVE","content":"string","tool":"string","input":"string","output":"string"}

Available Tools:
- get_weather(city:str): Takes city name as an input string and returns the weather info about the city
- run_command(cmd : str): Takes a system windows command as string and executes the command on users system and returns the output from the command
Example 1:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step":"PLAN", "content":"Seems like user is interested in Maths Problem"}
PLAN: {"step":"PLAN", "content":"Looking at the problem we can use BODMAS to solve"}
PLAN: {"step":"PLAN", "content":"yes,The BODMAS is the correct thing to use here"}
PLAN: {"step":"PLAN", "content":"we have * and /, so we come from left to right. First multiplication :3 *5 =15"}
PLAN: {"step":"PLAN", "content":"Lets do the division now: 15/10 =1.5"}
PLAN: {"step":"PLAN", "content":"Lets carry on with the addition : 2+1.5=3.5"}
PLAN: {"step":"PLAN", "content":"Great! we came to the answer as 3.5"}
OUTPUT: {"step":"OUTPUT","content":"3.5"}

Example 2:
START: What is the weather of Delhi?
PLAN: {"step":"PLAN", "content":"Seems like user is interested in knowing Delhis Weather"}
PLAN: {"step":"PLAN", "content":"Lets see if we have any available tools from the list of available tools"}
PLAN: {"step":"PLAN", "content":"Great! we have get_weather to get the weather of a city"}
PLAN: {"step":"PLAN", "content":"I need to call get_weather tool with the city name as input string"}
PLAN: {"step":"TOOL", "tool":"get_weather","input":"delhi"}
PLAN: {"step":"OBSERVE", "tool":"get_weather","output":"The delhis temperature is cloudy with 20 C"}
PLAN: {"step":"PLAN", "content":"Great! I got the weather info about the weather"}
OUTPUT: {"step":"OUTPUT","content":"The Current weather in delhi is 20 C with some cloudy sky"}

"""
print('\n\n\n')

class MyOutputFormat(BaseModel):
    step: str=Field(..., description="The ID of the step.Example: PLAN,OUTPUT,TOOL, etc")
    content: Optional[str] = Field(None,description="The optional string content for the step")
    tool: Optional[str]=Field(None,description="The ID of the tool to call")
    input:Optional[str]=Field(None,description="The input params for the tool")


history=[]
user_query=input("Ask your question- ")
history.append({"role":"user","parts": [{"text": user_query}]})

while True:
    if user_query.lower() == "exit":
        break
    response=client.models.generate_content(model="gemini-3.5-flash",contents=user_query,
                                            config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT,response_mime_type="application/json",response_schema=MyOutputFormat))
    history.append({"role":"model","parts": [{"text": response.text}]})
    print(response.text)
    parsed_result_list = [
        json.loads(line)
        for line in response.text.strip().splitlines()
        if line.strip()
    ]
    for parsed_result in parsed_result_list:
        if parsed_result.get("step")=="START":
            print("😊",parsed_result.get("content"))
            continue
        if parsed_result.get("step")=="TOOL":
            tool_to_call=parsed_result.get("tool")
            tool_input=parsed_result.get("input")
            print("Tool-",parsed_result.get("content"))
            continue
        if parsed_result.get("step")=="PLAN":
            print("🚀",parsed_result.get("content"))
            continue

        if parsed_result.get("step")=="OUTPUT":
            print("🤖",parsed_result.get("content"))
            break

    
    user_query=input("Ask your question- ")
    history.append({"role":"user","parts": [{"text": user_query}]})



