from fastapi import APIRouter, HTTPException
from rag.chromadb_client import get_collection
import json

router = APIRouter(prefix="/api/companies", tags=["Companies"])
collection = get_collection()

@router.get("/")
async def get_companies():
    try:
        # Retrieve all company data from ChromaDB where source = placement_cell
        results = collection.get(
            where={"source": "placement_cell"}
        )
        
        # We need to parse the text back into structured data or we could have stored it in metadata.
        # Since we stored company name in metadata, we can extract unique companies.
        companies = []
        for i in range(len(results["ids"])):
            meta = results["metadatas"][i]
            doc = results["documents"][i]
            
            # Simple parsing since we formatted it consistently in ingest.py
            # "Company: Amazon. Visit Date: 2024-08-15. Eligibility CGPA: 7.5..."
            company_data = {"name": meta.get("company")}
            
            # Extract basic info from the document string
            parts = doc.split(". ")
            for part in parts:
                if ": " in part:
                    k, v = part.split(": ", 1)
                    key_map = {
                        "Visit Date": "visit_date",
                        "Eligibility CGPA": "eligibility_cgpa",
                        "Package Range": "package_range",
                        "Number of Offers": "number_of_offers",
                        "Branches Allowed": "branches_allowed",
                        "Rounds": "rounds"
                    }
                    if k in key_map:
                        company_data[key_map[k]] = v.strip('.')
                        
            # Deduplicate by name
            if not any(c["name"] == company_data["name"] for c in companies):
                companies.append(company_data)
                
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}")
async def get_company_detail(name: str):
    try:
        results = collection.get(
            where={"$and": [{"source": "placement_cell"}, {"company": name}]}
        )
        
        if not results["ids"]:
            raise HTTPException(status_code=404, detail="Company not found")
            
        doc = results["documents"][0]
        meta = results["metadatas"][0]
        
        company_data = {"name": name}
        parts = doc.split(". ")
        for part in parts:
            if ": " in part:
                k, v = part.split(": ", 1)
                key_map = {
                    "Visit Date": "visit_date",
                    "Eligibility CGPA": "eligibility_cgpa",
                    "Package Range": "package_range",
                    "Number of Offers": "number_of_offers",
                    "Branches Allowed": "branches_allowed",
                    "Rounds": "rounds"
                }
                if k in key_map:
                    company_data[key_map[k]] = v.strip('.')
                    
        return company_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
