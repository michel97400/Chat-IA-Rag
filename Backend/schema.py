from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    evaluation: Optional[Dict[str, float]] = None

class EvaluationRequest(BaseModel):
    question: str
    answer: str
    contexts: List[str]

class EvaluationResponse(BaseModel):
    scores: Dict[str, float]
    global_score: float