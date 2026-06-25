from dotenv import load_dotenv
from google.genai import Client,types

from google.genai.types import GenerateContentConfig
from langchain_groq import ChatGroq
from langchain_qdrant import QdrantVectorStore
import os
load_dotenv()

client=Client(api_key=os.getenv('GOOGLE_API_KEY'))


embedding_model = lambda text: client.models.embed_content(
    model="gemini-embedding-2",
    contents=text,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768
    )
)

vector_db= QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

user_input=input("Ask Something")

search_results=vector_db.similarity_search(query=user_input)

context="\n\n\n".join([f"Page Content: {result.page_content}\n Page Number:{result.metadata['page_label']}\nFile location: {result.metadata['source']}"  for result in search_results])
SYSTEM_PROMPT=f"""

You are an helpful AI assistant who answers query based on the available context retrieved from a PDF along with page numbers.
You should only answer based on the following context and navigate the user to right page number to know more.

Context.
{context}
"""


response=client.models.generate_content(
    model="gemini-2.5-flash",
        contents=user_input,
        config=GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
)
print(f"Response:{response.candidates[0].content}")