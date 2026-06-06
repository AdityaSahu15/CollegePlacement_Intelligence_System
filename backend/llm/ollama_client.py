import os
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:8b")  # Override with OLLAMA_MODEL env var for local testing

# Initialize Ollama LLM
llm = OllamaLLM(
    base_url=OLLAMA_BASE_URL,
    model=MODEL_NAME,
    temperature=0.2
)

def get_llm():
    return llm
