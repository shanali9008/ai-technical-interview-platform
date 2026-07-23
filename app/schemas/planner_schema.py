from pydantic import BaseModel, Field
from typing import List, Literal


class InterviewPlan(BaseModel):
    candidate_summary: str = Field(
        ..., description="2-3 sentence summary of the candidate's fit for this role"
    )
    skills_found: List[str] = Field(
        default_factory=list,
        description="Short skill names present in both resume and job description, e.g. 'REST APIs'",
    )
    missing_skills: List[str] = Field(
        default_factory=list,
        description="Short skill names required by the job but missing/weak in the resume",
    )
    interview_topics: List[str] = Field(
        default_factory=list,
        description="Specific, askable topics, e.g. 'database indexing' not 'databases'",
    )
    difficulty: Literal["easy", "medium", "hard"]
    question_count: int = Field(default=10, ge=1, le=50)