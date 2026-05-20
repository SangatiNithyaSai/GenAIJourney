from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

client=OpenAI(
api_key=os.getenv('GOOGLE_API_KEY'),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

input_value=''
while input_value!='exit':
    input_value=input('Enter the question: To exit type \'exit\'')
    response=client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {'role':'system','content':'You are an expert in maths related queries only.If user asks question other that that just say sorry.If user types <exit> say Thank you!Bye,'},
            {'role':'user','content':str(input_value)}

        ]

    )
    print(response.choices[0].message.content)