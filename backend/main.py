from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv

from .routes import chat, companies, seniors, admin
from .rag.ingest import load_sample_data_if_empty

load_dotenv()

app = FastAPI(title="College Placement Intelligence System")

# CORS must be enabled for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Can restrict to localhost in dev, vercel URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

@app.on_event("startup")
async def startup_event():
    # Health check that verifies Ollama is reachable
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            if response.status_code != 200:
                print(f"WARNING: Ollama returned status {response.status_code}")
            else:
                print("Ollama health check passed on startup.")
    except Exception as e:
        print(f"CRITICAL: Ollama is not reachable at {OLLAMA_BASE_URL}. Error: {e}")
        # Note: We won't crash the server so admin can still hit it, but it's noted.

    # Auto-ingest sample data if ChromaDB is empty
    load_sample_data_if_empty()
    print("Startup complete. System ready.")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Placement Intelligence System"}

app.include_router(chat.router)
app.include_router(companies.router)
app.include_router(seniors.router)
app.include_router(admin.router)
