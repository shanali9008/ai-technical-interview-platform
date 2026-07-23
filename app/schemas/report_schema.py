from pydantic import BaseModel, Field
from typing import List, Literal


class InterviewReport(BaseModel):
    interview_score: int = Field(..., ge=0, le=100, description="Overall interview score, 0-100")
    decision: Literal["Hire", "Borderline", "No Hire"]
    summary: str = Field(..., description="3-5 sentences, plain prose")
    strengths: List[str] = Field(default_factory=list, description="Short, specific phrases")
    weaknesses: List[str] = Field(default_factory=list, description="Short, specific phrases")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Specific, actionable next steps tied to observed gaps — never generic advice like 'practice more'",
    )