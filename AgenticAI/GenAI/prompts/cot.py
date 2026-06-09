from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig
load_dotenv()
import json
client=genai.Client()

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
{"step": "START"|"PLAN"|"OUTPUT","content":"string"}

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step":"PLAN", "content":"Seems like user is interested in Maths Problem"}
PLAN: {"step":"PLAN", "content":"Looking at the problem we can use BODMAS to solve"}
PLAN: {"step":"PLAN", "content":"yes,The BODMAS is the correct thing to use here"}
PLAN: {"step":"PLAN", "content":"we have * and /, so we come from left to right. First multiplication :3 *5 =15"}
PLAN: {"step":"PLAN", "content":"Lets do the division now: 15/10 =1.5"}
PLAN: {"step":"PLAN", "content":"Lets carry on with the addition : 2+1.5=3.5"}
PLAN: {"step":"PLAN", "content":"Great! we came to the answer as 3.5"}
OUTPUT: {"step":"OUTPUT","content":"3.5"}



"""
print('\n\n\n')
history=[]
user_query=input("Ask your question- ")
history.append({"role":"user","parts": [{"text": user_query}]})

while True:
    if user_query.lower() == "exit":
        break
    response=client.models.generate_content(model="gemini-2.5-flash",contents=user_query,
                                            config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
    history.append({"role":"model","parts": [{"text": response.text}]})
    #print(response.text)
    parsed_result_list = [
        json.loads(line)
        for line in response.text.strip().splitlines()
        if line.strip()
    ]
    for parsed_result in parsed_result_list:
        if parsed_result.get("step")=="START":
            print("😊",parsed_result.get("content"))
            continue
        
        if parsed_result.get("step")=="PLAN":
            print("🚀",parsed_result.get("content"))
            continue

        if parsed_result.get("step")=="OUTPUT":
            print("🤖",parsed_result.get("content"))
            break

    
    user_query=input("Ask your question- ")
    history.append({"role":"user","parts": [{"text": user_query}]})
