from langchain_core.prompts import PromptTemplate
from rag.chromadb_client import get_collection
from llm.ollama_client import get_llm
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
collection = get_collection()
llm = get_llm()

# Define Prompt Template
PROMPT_TEMPLATE = """You are a placement assistant 
for [College Name]. You help students prepare for 
campus placements with specific, grounded advice.

STRICT RULES:
- Answer ONLY using the context provided below
- Assume the current year is 2026, so "last year" refers to 2025.
- Be specific — use exact numbers, dates, package 
  figures, and round details from context
- Never give generic advice not backed by context
- If context is insufficient say exactly: 
  "I don't have enough data on this yet."

CONTACT AND LINKEDIN RULES:
- If a student asks for contact details, 
  LinkedIn, phone number, email, or how 
  to reach a senior — carefully read all 
  "Contact:" lines in the context first
- If context contains "LinkedIn profile: [url]"
  for a senior → provide that URL directly 
  in your answer. Do not say you don't have 
  contact details if the URL is right there 
  in the context.
- If student asks for phone number or email:
  → respond exactly like this:
  "Phone/email is not available for [Name]. 
   However they have consented to be contacted 
   via LinkedIn: [url]"
- If context contains "has not consented to 
  share contact details":
  → respond exactly like this:
  "This senior has chosen not to share contact 
   details. You can still read their interview 
   experience above for preparation tips."
- Never fabricate a LinkedIn URL. Only share 
  URLs that are explicitly present in the context.
- If multiple seniors match (e.g. two Accenture 
  seniors) list all of them with their LinkedIn 
  URLs if available.

RESPONSE FORMAT RULES:
- For eligibility questions: always separate into
  three sections:
  ✅ Eligible: (list companies + their cutoff)
  ⚠️ Borderline: (within 0.5 CGPA of cutoff)  
  ❌ Not Eligible: (list companies + their cutoff)
  Then add actionable advice at the end.

- For company specific questions: give round by 
  round breakdown, then quote senior tips if 
  available in context, then suggest connecting 
  with seniors via Senior Network if their 
  experience is in context.

- For "who should I target" questions: rank 
  companies by fit, explain why each is a good 
  or bad match based on context data.

- For all questions: end with exactly 2 suggested 
  follow-up questions the student might want to ask,
  formatted as:
  💬 You might also ask:
  → "[question 1]"
  → "[question 2]"

- Always end with source citation:
  [Source: <specific sources used>]

Context:
{context}

Student Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

def classify_question(question: str) -> dict:
    """
    Classifies the question and returns smart 
    metadata filters for ChromaDB retrieval.
    """
    question_lower = question.lower()
    filters = {}
    
    # Known companies — extend this list as needed
    companies = [
        "amazon", "microsoft", "google", "deloitte",
        "tcs", "infosys", "wipro", "cisco", 
        "goldman sachs", "goldman", "atlassian",
        "adobe", "flipkart", "paytm", "zomato"
    ]
    
    for company in companies:
        if company in question_lower:
            # Match the exact casing stored in metadata
            filters["company"] = company.title()
            break
    
    # Senior network questions — filter to 
    # only consented seniors
    if any(word in question_lower for word in [
        "contact", "talk to", "connect", 
        "who got", "senior", "reach out",
        "linkedin", "message"
    ]):
        filters["source"] = "senior_experience"
        filters["consent"] = True
    
    # Eligibility / CGPA questions need broad 
    # search — no company filter
    if any(word in question_lower for word in [
        "cgpa", "eligible", "eligibility",
        "cutoff", "criteria", "ineligible",
        "which companies can i"
    ]):
        filters = {}
    
    # Time based questions — filter by year
    if "last year" in question_lower or "2025" in question_lower:
        filters["year"] = "2025"
    if "2024" in question_lower:
        filters["year"] = "2024"
    if "2023" in question_lower:
        filters["year"] = "2023"
    
    return filters

def retrieve_and_generate(question: str, metadata_filters: dict = None):
    """
    Retrieves context from ChromaDB based on the question and filters,
    and generates an answer using Qwen3 via Ollama.
    """
    
    if not metadata_filters:
        metadata_filters = classify_question(question)
        
    # 1. Embed the question
    query_embedding = embedding_model.embed_query(question)
    
    # 2. Query ChromaDB
    # If metadata_filters is provided and has items, apply them
    where_clause = None
    if metadata_filters:
        # ChromaDB 'where' clause format
        # If there's only one filter, just use it.
        # If multiple, use {"$and": [{k: v}, ...]}
        if len(metadata_filters) == 1:
            where_clause = metadata_filters
        else:
            where_clause = {"$and": [{k: v} for k, v in metadata_filters.items()]}
            
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=8,
        where=where_clause
    )
    
    # 3. Format context and extract sources
    contexts = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    
    if not contexts:
        return {
            "answer": "I don't have enough data about this yet.",
            "sources": []
        }
        
    context_str = "\n\n".join(contexts)
    
    # Extract unique sources for the citation
    sources = []
    for meta in metadatas:
        source_type = meta.get("source", "unknown")
        company = meta.get("company", "")
        year = meta.get("year", "")
        batch = meta.get("year", "")
        
        if source_type == "placement_cell":
            label = f"Placement cell data"
            if company:
                label += f" for {company}"
            if year:
                label += f" ({year})"
            sources.append(label)
            
        elif source_type == "senior_experience":
            label = f"Senior experience"
            if company:
                label += f" at {company}"
            if batch:
                label += f", Batch {batch}"
            sources.append(label)
            
        else:
            sources.append("Uploaded document")

    unique_sources = list(set(sources))
    sources_str = ", ".join(unique_sources)
    
    # Check if the context contains enough information is handled by the LLM via prompt,
    # but we can optionally add the sources to the context for it to use, or just append ourselves.
    # The prompt asks the LLM to end with [Source: ...], we will provide the sources string in the context 
    # or let the LLM extract it. Actually, the prompt says "mention the sources used".
    # We will inject the sources into the context so the LLM knows what they are.
    
    context_with_sources = (
        f"{context_str}\n\n"
        f"Available sources: {sources_str}"
    )

    # 4. Generate answer
    formatted_prompt = prompt.format(
        context=context_with_sources, 
        question=question
    )
    
    answer = llm.invoke(formatted_prompt)
    
    import re
    # Qwen3 sometimes leaks <think> tags — strip them
    answer = re.sub(
        r'<think>.*?</think>', 
        '', 
        answer, 
        flags=re.DOTALL
    ).strip()

    # Basic validation
    if not answer or len(answer.strip()) < 20:
        return {
            "answer": "I don't have enough data on this yet.",
            "sources": []
        }
    
    # Post-process: ensure the answer ends with a source if the LLM failed to format it properly,
    # though Qwen is usually good at following instructions.
    
    return {
        "answer": answer,
        "sources": unique_sources
    }
