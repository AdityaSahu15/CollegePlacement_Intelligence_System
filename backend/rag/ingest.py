import json
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .chromadb_client import get_collection

# Embedding model to use
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
collection = get_collection()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def ingest_pdf(file_path: str, source_metadata: dict):
    """Ingests a PDF file into ChromaDB."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)
    
    # Add metadata to chunks
    for chunk in chunks:
        chunk.metadata.update(source_metadata)
    
    # Extract text and metadata for ChromaDB
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [f"{file_path}_{i}" for i in range(len(chunks))]
    
    # Embeddings are computed and stored automatically by LangChain Chroma if we were using it,
    # but since we use raw chromadb client, we need to embed manually or use a langchain wrapper.
    # Actually, using chromadb directly is easier for explicit metadata filtering if we configure its embedding function.
    # Let's embed manually using HuggingFaceEmbeddings
    embeddings = embedding_model.embed_documents(texts)
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    return len(chunks)

def ingest_senior_experience(experience: dict):
    """Ingests a structured senior experience dict into ChromaDB."""
    text = (f"Name: {experience.get('name')}, Batch: {experience.get('batch')}. "
            f"Cleared {experience.get('company')} as {experience.get('role')}. "
            f"Rounds: {experience.get('rounds_detail')}. "
            f"Questions Asked: {experience.get('questions_asked')}. "
            f"Tech Stack: {experience.get('tech_stack')}. "
            f"Tips: {experience.get('tips')}.")
            
    metadata = {
        "source": "senior_experience",
        "company": experience.get("company", ""),
        "year": experience.get("batch", ""),
        "consent": experience.get("consent", False),
        "selected": experience.get("selected", False),
        "linkedin_url": experience.get("linkedin_url", "")
    }
    
    # Since it's a short text, maybe one chunk is fine. But let's split just in case.
    chunks = text_splitter.split_text(text)
    texts = chunks
    metadatas = [metadata for _ in chunks]
    
    # Use a unique ID based on name and company
    base_id = f"senior_{experience.get('name', 'unknown')}_{experience.get('company', 'unknown')}".replace(" ", "_")
    ids = [f"{base_id}_{i}" for i in range(len(chunks))]
    
    embeddings = embedding_model.embed_documents(texts)
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    return len(chunks)

def ingest_company_data(company: dict):
    """Ingests structured company info into ChromaDB."""
    text = (f"Company: {company.get('name')}. "
            f"Visit Date: {company.get('visit_date')}. "
            f"Eligibility CGPA: {company.get('eligibility_cgpa')}. "
            f"Branches Allowed: {', '.join(company.get('branches_allowed', []))}. "
            f"Rounds: {company.get('rounds')}. "
            f"Package Range: {company.get('package_range')}. "
            f"Number of Offers: {company.get('number_of_offers')}.")
            
    metadata = {
        "source": "placement_cell",
        "company": company.get("name", ""),
        "cgpa_cutoff": str(company.get("eligibility_cgpa", ""))
    }
    
    chunks = text_splitter.split_text(text)
    texts = chunks
    metadatas = [metadata for _ in chunks]
    
    base_id = f"company_{company.get('name', 'unknown')}".replace(" ", "_")
    ids = [f"{base_id}_{i}" for i in range(len(chunks))]
    
    embeddings = embedding_model.embed_documents(texts)
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    return len(chunks)

def load_sample_data_if_empty():
    """Checks if ChromaDB is empty, if so, loads sample data."""
    if collection.count() > 0:
        return
        
    print("ChromaDB is empty. Auto-ingesting sample data...")
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sample")
    
    # Ingest companies
    try:
        with open(os.path.join(sample_dir, "sample_companies.json"), "r") as f:
            companies = json.load(f)
            for c in companies:
                ingest_company_data(c)
        print(f"Ingested {len(companies)} sample companies.")
    except Exception as e:
        print(f"Error ingesting sample companies: {e}")
        
    # Ingest seniors
    try:
        with open(os.path.join(sample_dir, "sample_seniors.json"), "r") as f:
            seniors = json.load(f)
            for s in seniors:
                ingest_senior_experience(s)
        print(f"Ingested {len(seniors)} sample senior experiences.")
    except Exception as e:
        print(f"Error ingesting sample seniors: {e}")
        
    # PDF ingestion skipped for mock, unless we have a real PDF.
    print("Sample data auto-ingestion complete.")
