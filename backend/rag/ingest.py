import json
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from rag.chromadb_client import get_collection

# Embedding model to use
_embedding_model = None
def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding_model
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
    import hashlib
    ids = [
        hashlib.md5(
            f"{file_path}_{chunk.page_content}".encode()
        ).hexdigest()
        for chunk in chunks
    ]
    
    # Embeddings are computed and stored automatically by LangChain Chroma if we were using it,
    # but since we use raw chromadb client, we need to embed manually or use a langchain wrapper.
    # Actually, using chromadb directly is easier for explicit metadata filtering if we configure its embedding function.
    # Let's embed manually using HuggingFaceEmbeddings
    embeddings = get_embedding_model().embed_documents(texts)
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    return len(chunks)

def ingest_senior_experience(experience: dict):
    """Ingests a structured senior experience dict into ChromaDB."""
    consent = experience.get("consent", False)
    linkedin = experience.get("linkedin_url", "")

    if consent and linkedin:
        contact_info = (
            f"Contact: This senior has consented to "
            f"be contacted by juniors. "
            f"LinkedIn profile: {linkedin}"
        )
    else:
        contact_info = (
            f"Contact: This senior has not consented "
            f"to share contact details. No LinkedIn "
            f"or phone number available."
        )

    text = (
        f"{experience.get('name')} from batch "
        f"{experience.get('batch')} was "
        f"{'selected' if experience.get('selected') else 'not selected'} "
        f"at {experience.get('company')} for the "
        f"role of {experience.get('role')}. "
        f"The interview had the following rounds: "
        f"{experience.get('rounds_detail')}. "
        f"Questions that were asked: "
        f"{experience.get('questions_asked')}. "
        f"Their tech stack was: {experience.get('tech_stack')}. "
        f"Their advice for juniors: {experience.get('tips')}. "
        f"{contact_info}"
    )
            
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
    
    embeddings = get_embedding_model().embed_documents(texts)
    
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
        "cgpa_cutoff": str(company.get("eligibility_cgpa", "")),
        "visit_date": company.get("visit_date", ""),
        "year": str(company.get("visit_date", ""))[:4]
    }
    
    chunks = text_splitter.split_text(text)
    texts = chunks
    metadatas = [metadata for _ in chunks]
    
    base_id = f"company_{company.get('name', 'unknown')}".replace(" ", "_")
    ids = [f"{base_id}_{i}" for i in range(len(chunks))]
    
    embeddings = get_embedding_model().embed_documents(texts)
    
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
                try:
                    ingest_company_data(c)
                except Exception as e:
                    print(f"Failed to ingest {c.get('name')}: {e}")
                    continue
        print(f"Ingested {len(companies)} sample companies.")
    except Exception as e:
        print(f"Error loading sample companies: {e}")
        
    # Ingest seniors
    try:
        with open(os.path.join(sample_dir, "sample_seniors.json"), "r") as f:
            seniors = json.load(f)
            for s in seniors:
                try:
                    ingest_senior_experience(s)
                except Exception as e:
                    print(f"Failed to ingest senior {s.get('name')}: {e}")
                    continue
        print(f"Ingested {len(seniors)} sample senior experiences.")
    except Exception as e:
        print(f"Error loading sample seniors: {e}")
        
    # PDF ingestion skipped for mock, unless we have a real PDF.
    print("Sample data auto-ingestion complete.")

def clear_and_reingest_seniors():
    """
    Clears all senior_experience entries from 
    ChromaDB and re-ingests from sample JSON.
    Run this once after updating ingest logic
    to ensure LinkedIn URLs are in document text.
    """
    try:
        collection.delete(
            where={"source": "senior_experience"}
        )
        print("Cleared old senior experiences from ChromaDB.")
    except Exception as e:
        print(f"Error clearing seniors: {e}")
    
    sample_dir = os.path.join(
        os.path.dirname(__file__), 
        "..", "data", "sample"
    )
    
    try:
        with open(
            os.path.join(sample_dir, "sample_seniors.json"), "r"
        ) as f:
            seniors = json.load(f)
            success = 0
            for s in seniors:
                try:
                    ingest_senior_experience(s)
                    success += 1
                except Exception as e:
                    print(f"Failed to ingest {s.get('name')}: {e}")
                    continue
            print(f"Re-ingested {success}/{len(seniors)} seniors.")
            print("LinkedIn URLs are now embedded in document text.")
    except Exception as e:
        print(f"Error loading sample_seniors.json: {e}")
