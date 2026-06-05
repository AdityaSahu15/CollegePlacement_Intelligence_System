<<<<<<< HEAD
# College Placement Intelligence System

A RAG-based web application that serves as a private placement preparation assistant for college students. It uses local placement cell data and senior experiences to answer any placement-related questions. 

## Why I Built This
As a student navigating the placement season, I realized that generic internet advice doesn't apply to specific campus drives. Every college has its own patterns, eligibility criteria, and past trends. I built this tool to centralize all that scattered data (PDFs, Excel sheets, senior chats) into one intelligent, queryable assistant so nobody goes into an interview blind.

## How to Run It

### Prerequisites
- Python 3.9+
- Node.js 18+
- Ollama installed locally

### Step 1: Start Ollama
Ensure Ollama is running the `qwen3:8b` model locally.
```bash
ollama run qwen3:8b
```

### Step 2: Start the Backend
Open a terminal in the `backend` directory.
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*Note: On the first run, the system will automatically ingest sample data into ChromaDB.*

### Step 3: Start the Frontend
Open another terminal in the `frontend` directory.
``bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173` in your browser.

## Architecture Decisions
- **Local LLM (Qwen3-8B via Ollama)**: Ensures 100% data privacy. College placement data never leaves the server, eliminating data leakage risks and API costs.
- **ChromaDB**: Chosen for its robust metadata filtering capabilities, allowing the system to accurately filter searches by specific companies or years before passing context to the LLM.
- **No Public Data**: The system exclusively uses verified internal placement cell documents and consented senior experiences. This prioritizes specificity and accuracy over generic web advice.
- **RAG over Fine-tuning**: Allows for continuous, dynamic updates (like new senior form submissions or new PDF uploads) without the immense cost and time of retraining the model.

## AI Usage
AI was extensively used during the development of this project. Specifically, an AI agent assisted in architecting the RAG pipeline, generating the complex FastAPI endpoints, and rapidly prototyping the modern React/Tailwind frontend. AI was instrumental in ensuring best practices for both the LangChain integration and UI design.

## Future Plans (With 4 More Weeks)
- **Multi-college Support**: Scale the database architecture to partition data by college domains.
- **Resume Upload**: Add a feature where students can upload their resumes to get personalized company shortlists based on past selection trends.
- **Auto-ingestion**: Integrate directly with the university placement portal to auto-sync new job postings.
- **Analytics Dashboard**: Build an advanced dashboard for the placement cell to track student readiness and common queries.
- **Mobile App**: Port the React frontend to React Native for on-the-go access.
=======
# College-Placement-Intelligence-System
>>>>>>> bd39c3df44ee4bf36f31fd867f1b4ff163c5003f
