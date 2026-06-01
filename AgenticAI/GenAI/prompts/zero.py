from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai.types import GenerateContentConfig
client=genai.Client()
from rich import print

SYSTEM_PROMPT="You should only answers questions related to coding. If the user asks any other questions,just say I cant answer it in your style."
while True:
   user_query=input("Enter your ques:\n >")
   if user_query.lower() == "exit":
      break
   response=client.models.generate_content(model="gemini-3.5-flash",
                                        contents=user_query,
                                        config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
   print(response.text)