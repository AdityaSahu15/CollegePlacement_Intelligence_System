from fastapi import APIRouter, HTTPException, Query
from models.schemas import SeniorExperienceForm
from rag.chromadb_client import get_collection
from rag.ingest import ingest_senior_experience
from typing import Optional

router = APIRouter(prefix="/api/seniors", tags=["Seniors"])
collection = get_collection()

@router.get("/")
async def get_seniors(
    company: Optional[str] = None,
    batch: Optional[str] = None,
    consent: Optional[bool] = None
):
    try:
        where_filters = [{"source": "senior_experience"}]
        
        if company:
            where_filters.append({"company": company})
        if batch:
            where_filters.append({"year": batch})
        if consent is not None:
            where_filters.append({"consent": consent})
            
        where_clause = {"$and": where_filters} if len(where_filters) > 1 else where_filters[0]
        
        results = collection.get(where=where_clause)
        
        seniors = []
        for i in range(len(results["ids"])):
            meta = results["metadatas"][i]
            doc = results["documents"][i]
            
            # Simple extraction from doc string
            senior_data = {
                "company": meta.get("company"),
                "batch": meta.get("year"),
                "consent": meta.get("consent"),
                "selected": meta.get("selected")
            }
            
            # Show linkedin only if consent is true
            if meta.get("consent"):
                senior_data["linkedin_url"] = meta.get("linkedin_url", "")
            
            parts = doc.split(". ")
            for part in parts:
                if ": " in part:
                    k, v = part.split(": ", 1)
                    key_map = {
                        "Name": "name",
                        "Batch": "batch_from_doc",
                        "Cleared": "cleared",
                        "Rounds": "rounds_detail",
                        "Questions Asked": "questions_asked",
                        "Tech Stack": "tech_stack",
                        "Tips": "tips"
                    }
                    if k in key_map:
                        senior_data[key_map[k]] = v.strip('.')
                        
            # Handle the "Cleared X as Y" case from ingest.py
            if "Cleared " in doc and " as " in doc:
                # Basic parsing, good enough for mock
                senior_data["role"] = doc.split(" as ")[1].split(". ")[0]
            else:
                senior_data["role"] = "Unknown"
                
            # Prevent duplicate chunks from the same senior
            if not any(s.get("name") == senior_data.get("name") for s in seniors):
                seniors.append(senior_data)
                
        return seniors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contribute")
async def contribute_experience(form_data: SeniorExperienceForm):
    try:
        chunks_added = ingest_senior_experience(form_data.dict())
        return {"success": True, "chunks_added": chunks_added}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
