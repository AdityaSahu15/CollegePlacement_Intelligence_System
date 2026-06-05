from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import os
import shutil
from ..rag.chromadb_client import get_collection
from ..rag.ingest import ingest_pdf
from ..models.schemas import StatsResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/admin", tags=["Admin"])
collection = get_collection()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

@router.post("/upload")
async def upload_document(
    password: str = Form(...),
    file: UploadFile = File(...)
):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
        
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    try:
        # Save temp file
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest PDF
        metadata = {"source": "placement_cell"}
        chunks_added = ingest_pdf(temp_file_path, metadata)
        
        # Clean up
        os.remove(temp_file_path)
        
        return {"success": True, "chunks_added": chunks_added, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    try:
        # We can approximate stats by filtering based on source
        # ChromaDB `count` gives total chunks
        total_chunks = collection.count()
        
        # We fetch all metadata to compute distinct companies and seniors count
        # In a real app with large DB, we wouldn't fetch everything, maybe keep separate DB counters
        results = collection.get()
        metadatas = results.get("metadatas", [])
        
        companies_set = set()
        seniors_set = set()
        
        for meta in metadatas:
            source = meta.get("source")
            if source == "placement_cell" and meta.get("company"):
                companies_set.add(meta.get("company"))
            elif source == "senior_experience" and meta.get("company"):
                # Unique senior could be approximated by looking at the document ID base,
                # but since we didn't save name explicitly in metadata, we can just count "senior_experience" chunks
                # For more accuracy, we could store name in metadata
                pass
                
        # To get distinct senior count, we can filter for source=senior_experience and just assume each document
        # represents 1 chunk since we split, or we look at unique ids.
        senior_results = collection.get(where={"source": "senior_experience"})
        senior_ids = senior_results.get("ids", [])
        unique_senior_ids = set()
        for s_id in senior_ids:
            # ids are like senior_name_company_0
            base = "_".join(s_id.split("_")[:-1])
            unique_senior_ids.add(base)
            
        return StatsResponse(
            total_docs=total_chunks,
            companies_count=len(companies_set),
            seniors_count=len(unique_senior_ids)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
