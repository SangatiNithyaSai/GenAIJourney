import os
from dotenv import load_dotenv
#embedding model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
##Data Ingestion
from llama_index.readers.web import SimpleWebPageReader
#Data indexing
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
load_dotenv()

embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model=embed_model
url="https://wlockett.medium.com/ai-pullback-has-officially-started-fb6dfa5e4128"


from llama_index.llms.groq import Groq
Settings.llm=Groq(model="openai/gpt-oss-120b")
documents=SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
print(f"Loaded {len(documents)} Documents")
print(documents)

index=VectorStoreIndex.from_documents(documents=documents)
engine=index.as_query_engine()
response=engine.query("Tell me about the document")
print(response)