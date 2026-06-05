from langchain.prompts import PromptTemplate
from .chromadb_client import get_collection
from ..llm.ollama_client import get_llm
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
collection = get_collection()
llm = get_llm()

# Define Prompt Template
PROMPT_TEMPLATE = """You are a placement assistant for College.
Answer ONLY using the context provided below.
If the context doesn't contain enough information,
say "I don't have enough data about this yet."
Always end your answer with:
[Source: <mention the sources used>]
Be specific. Use numbers and facts from context.

Context: {context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

def retrieve_and_generate(question: str, metadata_filters: dict = None):
    """
    Retrieves context from ChromaDB based on the question and filters,
    and generates an answer using Qwen3 via Ollama.
    """
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
        n_results=5,
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
        if source_type == "placement_cell":
            sources.append(f"Placement cell data for {company}" if company else "Placement cell data")
        elif source_type == "senior_experience":
            sources.append(f"Senior experience for {company}" if company else "Senior experience")
        else:
            sources.append("Document upload")
            
    # Deduplicate sources
    unique_sources = list(set(sources))
    sources_str = ", ".join(unique_sources)
    
    # Check if the context contains enough information is handled by the LLM via prompt,
    # but we can optionally add the sources to the context for it to use, or just append ourselves.
    # The prompt asks the LLM to end with [Source: ...], we will provide the sources string in the context 
    # or let the LLM extract it. Actually, the prompt says "mention the sources used".
    # We will inject the sources into the context so the LLM knows what they are.
    
    augmented_context = context_str + f"\n\nAVAILABLE SOURCES FOR THESE FACTS: {sources_str}"
    
    # 4. Generate answer
    formatted_prompt = prompt.format(context=augmented_context, question=question)
    
    answer = llm.invoke(formatted_prompt)
    
    # Post-process: ensure the answer ends with a source if the LLM failed to format it properly,
    # though Qwen is usually good at following instructions.
    
    return {
        "answer": answer,
        "sources": unique_sources
    }
