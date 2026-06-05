import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# Initialize persistent client
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_chroma_client():
    return chroma_client

def get_collection(collection_name="placement_data"):
    return chroma_client.get_or_create_collection(name=collection_name)
