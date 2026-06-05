import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "qwen3:8b" # As requested by architecture decisions

# Initialize Ollama LLM
llm = Ollama(
    base_url=OLLAMA_BASE_URL,
    model=MODEL_NAME,
    temperature=0.2  # Low temp for grounded answers
)

def get_llm():
    return llm
