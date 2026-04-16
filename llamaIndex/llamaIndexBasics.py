from dotenv import load_dotenv
from llama_index.llms.groq import Groq
import os

load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

def main():
    print("Hello from llamaindex!")
    response=Groq(model="openai/gpt-oss-120b",api_key=os.environ["GROQ_API_KEY"]).complete("What is LlamaIndex")
    print(response)
     
if __name__ == "__main__":
    main()
