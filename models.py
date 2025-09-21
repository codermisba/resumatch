# models.py
from pydantic import BaseModel
from typing import List

class Result(BaseModel):
    candidate: str
    job_id: str
    score: float
    verdict: str
    missing: List[str]
