from langchain_core.prompts import PromptTemplate
from rag.chromadb_client import get_collection
from llm.ollama_client import get_llm
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
collection = get_collection()
llm = get_llm()

# Define Prompt Template
PROMPT_TEMPLATE = """You are a placement 
assistant for College Name. You help students 
prepare for campus placements with specific, 
grounded, honest advice.

STRICT RULES:
- Answer ONLY using the context provided below
- Be specific — use exact numbers, dates, 
  package figures, round details from context
- Never give generic advice not backed by context
- If context is insufficient say exactly:
  "I don't have enough data on this yet."
- Never use markdown bold (**text**) anywhere
- Never use markdown italic (*text*) anywhere  
- Never use markdown headers (##, ###) anywhere
- Never write [url] as a placeholder — either 
  write the actual URL from context or say 
  "LinkedIn URL not available"
- Never fabricate data not present in context

ELIGIBILITY QUESTION RULES:
- Always show ALL companies from context,
  not just a few
- Separate into three clear sections:
  Eligible: (company — cutoff CGPA — package range)
  Borderline: (within 0.5 CGPA of cutoff)
  Not Eligible: (company — cutoff CGPA)
- After the sections add one line of 
  actionable advice
- If a company allows "All Branches" it is 
  eligible for every student regardless of branch

COMPANY QUESTION RULES:
- Give round by round breakdown clearly
- Quote senior tips word for word if available
- Mention senior name and batch when quoting
- If senior has LinkedIn in context, show it
- Suggest connecting via Senior Network

CONTACT AND LINKEDIN RULES:
- Read context carefully for lines starting 
  with "Contact:"
- If context says "LinkedIn profile: https://..."
  copy that exact URL. Do not paraphrase it.
- If student asks for phone/email:
  Say "Phone and email are not available for 
  [Name]. You can reach them via LinkedIn: 
  [actual url from context]"
- If senior has not consented:
  Say "This senior has not shared contact 
  details, but here is their interview 
  experience for your preparation."
- If consent=true but no URL somehow:
  Say "This senior consented but LinkedIn URL 
  is not available in our records."

BROAD QUESTION RULES:
- For "which companies visited" — list ALL 
  companies found in context with visit dates
- For "consulting companies" — filter by 
  company type if available, else include all
- For "hardest company" — reason from number 
  of offers, CGPA cutoff, and number of rounds
- For "easiest to crack" — reason from offers 
  made, CGPA cutoff, and round difficulty

RESPONSE STYLE RULES:
- Plain text only. No bold, no italic, 
  no markdown headers
- Emojis for sections are fine: ✅ ⚠️ ❌ 💬 📎
- Be direct. Don't start with "Certainly!" 
  or "Great question!"
- End every response with exactly 2 follow-up 
  questions formatted as:
  You might also ask:
  -> "[question 1]"
  -> "[question 2]"
- Always end with source citation:
  [Source: specific sources used]

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
    
    broad_keywords = [
        "all companies", "visited", "last year",
        "consulting", "product compan", 
        "service compan", "hardest", "easiest",
        "highest package", "lowest package",
        "most offers", "which companies offer",
        "which companies allow", "which companies visit"
    ]

    if any(word in question_lower for word in broad_keywords):
        return {}

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
            
    question_lower = question.lower()
    is_eligibility_question = any(word in question_lower 
        for word in [
            "cgpa", "eligible", "eligibility", 
            "cutoff", "ineligible", "which companies can",
            "which companies am i", "apply to",
            "allow", "branches"
        ])

    is_broad_question = any(word in question_lower 
        for word in [
            "all companies", "visited", "last year",
            "consulting", "product companies", 
            "service companies", "highest package",
            "lowest", "most offers"
        ])

    n_results = 5

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
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
