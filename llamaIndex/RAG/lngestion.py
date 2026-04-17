from dotenv import load_dotenv
from llama_index.core import Document
from llama_index.core import Settings
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.groq import Groq
#Text Splitters - called as Nodes
from llama_index.core.node_parser import SentenceSplitter
#vector store
from llama_index.core import VectorStoreIndex

load_dotenv()
#os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model=embed_model
Settings.llm=Groq(model="openai/gpt-oss-120b")
Settings.chunk_size=512
#Load the data
documents= SimpleDirectoryReader(
    input_dir="../llamaindex-docs",
    recursive=False,
    required_exts=[".md"],
    num_files_limit=20
).load_data()

index=VectorStoreIndex.from_documents(documents=documents)

#query
engine=index.as_query_engine()
response=engine.query("What is Pinecone")
print(response)
