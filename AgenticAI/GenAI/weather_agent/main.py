from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig
load_dotenv()
import requests
client=genai.Client()


def get_weather(city:str):
    """ This function is used for retrieving the weather status of the provided city"""
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response= requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"


while True:

    user_query=input("Ask your question- ")
    if user_query.lower() == "exit":
        break
    response=client.models.generate_content(model="gemini-3.5-flash",contents=user_query,
                                            config=GenerateContentConfig(tools=[get_weather],temperature=0.4))
    print("Response:",response.text)
