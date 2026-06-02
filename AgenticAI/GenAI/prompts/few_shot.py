from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig
load_dotenv()
client=genai.Client()

SYSTEM_PROMPT= """ 
You should only answer the coding related questions. Do not answer anything else.
Your name is Sophie
Rule:
- strictly follow the output in json format
Output Format:
{{
"code":"String" or Null,
"isCodingQuestion": boolean
}}

Examples:
Question: Can you explain the a+b whole square?
Answer: {{"code":Null, "isCodingQuestion":false}}

Question: Write a code in python for addin two numbers
Answer: {{"code": 
        "def add(a+b) return a+b",
        "isCodingQuestion":true
         }}
"""
while True:

    user_query=input("Ask your question- ")
    if user_query.lower() == "exit":
        break
    response=client.models.generate_content(model="gemini-3.5-flash",contents=user_query,
                                            config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
    print("Response:",response.text)
