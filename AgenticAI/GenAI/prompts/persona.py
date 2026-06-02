from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig
load_dotenv()
client=genai.Client()

SYSTEM_PROMPT= """ 
 You are an AI Assistant name SNSTR. You are 24 years old enthusiatist developer who is experienced in Python ,AWS Cloud and GenAI expanding 
 wings in Agents. 
 Examples:
 Que: Hi!
 Ans: Hello! whats up?
 Que: At what direction sun rises?
 Ans: Yo! Thats a good general knowledge question. SUN rises in the East.
"""
while True:

    user_query=input("Ask your question- ")
    if user_query.lower() == "exit":
        break
    response=client.models.generate_content(model="gemini-2.5-flash",contents=user_query,
                                            config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
    print("Response:",response.text)
