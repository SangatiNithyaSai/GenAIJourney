from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

model=ChatGroq(model="openai/gpt-oss-20b")

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Translate the following into {language}"),
        ("user","{text}")
    ]
)

output=StrOutputParser()
chain=prompt|model|output

#App definition

app=FastAPI(title="LangChain Server",
            version="1.0",
            description="A simple API server using LangChain runnable interfaces")

#adding the routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)


### Steps after deployment
'''
1. To see the docs for API links ,go to http://127.0.0.1:8000/docs 
2. To directly use the app go to http://127.0.0.1:8000/chain/playground
3. To validate the response via curl --
curl -X POST http://127.0.0.1:8000/chain/invoke \
     -H "Content-Type: application/json" \
     -d '{
          "input": {
            "text": "Happy Ugadi",
           "language": "Telugu"
        },
         "config": {},
         "kwargs": {
           "additionalProp1": {}
         }
       }'

'''