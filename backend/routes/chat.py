from fastapi import APIRouter, HTTPException
from ..models.schemas import ChatRequest, ChatResponse
from ..rag.pipeline import retrieve_and_generate

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Determine if we should apply any metadata filters based on the question (simple heuristic)
        # For a production app, we might use an LLM or NER to extract company names from the query.
        # Here we'll just do a semantic search across all data unless a filter is explicitly needed.
        filters = {}
        
        # Example heuristic: if "Amazon" is in the question, filter by Amazon.
        # But semantic search usually handles this well enough without strict filtering.
        # The requirements say "Metadata filters applied where relevant (e.g. company filter for company-specific questions)"
        # Let's add a basic keyword check for demonstration.
        lower_q = request.question.lower()
        if "amazon" in lower_q:
            filters["company"] = "Amazon"
        elif "deloitte" in lower_q:
            filters["company"] = "Deloitte"
        elif "tcs" in lower_q:
            filters["company"] = "TCS"
        # In a real scenario, we'd fetch all companies and check, but this is a simplified heuristic.

        # If no strict filters identified, pass None
        result = retrieve_and_generate(
            question=request.question,
            metadata_filters=filters if filters else None
        )
        return ChatResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
