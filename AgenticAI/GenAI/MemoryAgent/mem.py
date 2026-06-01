from dotenv import load_dotenv
load_dotenv()
import os
import json
from mem0 import Memory

from google.genai.types import GenerateContentConfig

# 1. Retrieve the correct API key
api_key = os.getenv('GOOGLE_API_KEY')
from google import genai

client=genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


# Initialize the OpenAI compatibility client for Gemini

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": api_key,
            "model": "gemini-embedding-001" , # Google's standard embedding model
            "output_dimensionality": 1536
        }
    }
    ,
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": api_key,
            "model": "gemini-2.5-flash"   # Or "gemini-1.5-pro" depending on your preference
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://ad4bf8fd.databases.neo4j.io",
            "username": "ad4bf8fd",
            "password": os.getenv("neo4j_PSWD")  # Make sure to populate this
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input(">Enter the question \n type exit or quit to stop the conversation : ")
    if user_query.lower() in ['exit', 'quit']:
        break

    search_memory = mem_client.search(query=user_query, filters={"user_id":"nithyasai"})
    
    # Safely handle extraction based on Mem0 memory object schemas
    memories = [
        f"ID: {mem.get('id') if isinstance(mem, dict) else mem.id}\nMemory: {mem.get('memory') if isinstance(mem, dict) else mem.memory}"
        for mem in search_memory.get("results", [])
    ]
    print("Found Memory:", memories)

    SYSTEM_PROMPT = f"""
     You are a helpful assistant. Here is the recovered long-term context about the user:
     {json.dumps(memories)}
    """
    
    # FIXED: Corrected the typo "comtent" to "content"
    messages = [
        {"role": "user", "parts": [{"text":user_query}]}
    ]
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    
    ai_response = response.text
    print("Ai:", ai_response)
    mem_client.add(
        user_id="nithyasai",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    print("Memory has been saved\n" + "-"*20)