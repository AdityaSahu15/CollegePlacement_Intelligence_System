from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    college: Optional[str] = None # For future multi-college support

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class SeniorExperienceForm(BaseModel):
    name: str
    batch: str
    company: str
    role: str
    rounds_detail: str
    questions_asked: str
    tech_stack: str
    tips: str
    linkedin_url: Optional[str] = ""
    consent: bool
    selected: bool

class StatsResponse(BaseModel):
    total_docs: int
    companies_count: int
    seniors_count: int
