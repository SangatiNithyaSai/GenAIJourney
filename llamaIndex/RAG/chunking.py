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
Settings.chunk_overlap=50
#Load the data
documents= SimpleDirectoryReader(
    input_dir="../llamaindex-docs",
    recursive=False,
    required_exts=[".md"],
    num_files_limit=20
).load_data()
#Splitting
nodes_parser=SentenceSplitter(
 chunk_size=Settings.chunk_size,
 chunk_overlap=Settings.chunk_overlap
)
#split the nodes
print(f"Parsing documents into nodes with chunk size:{Settings.chunk_size}")
nodes=nodes_parser.get_nodes_from_documents(documents)
print(f"The document is spilt into {len(nodes)} nodes")
print("Sample nodes after custom chunking")

for i,node in enumerate(nodes[:3]):
    print(f"Node {i+1} Content : {node.get_content}")

    if node.metadata:
        print(f"-source: {node.metadata.get('file_name','N/A')}")
        

print("Creating Vector store from Nodes")
index=VectorStoreIndex(nodes)
print('vector store is created')

#query
engine=index.as_query_engine()
response=engine.query("What can Agents do?")
print(response)
