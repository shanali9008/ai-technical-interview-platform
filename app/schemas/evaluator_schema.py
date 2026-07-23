from pydantic import BaseModel, Field
from typing import List, Literal


class AnswerEvaluation(BaseModel):
    score: int = Field(..., ge=0, le=10, description="0 = completely incorrect or blank, 10 = complete and accurate for the given difficulty")
    strengths: List[str] = Field(default_factory=list, description="Short phrases, not full sentences")
    weaknesses: List[str] = Field(default_factory=list, description="Short phrases, not full sentences")
    follow_up_required: bool
    reason: str = Field(..., description="One sentence explaining the chosen next_action")
    next_action: Literal["follow_up", "next_question"]