from pydantic import BaseModel, Field
from typing import Optional


class InterviewerTurn(BaseModel):
    message: str = Field(
        ..., description="The single next message to send to the candidate — greeting, question, or follow-up. Exactly one question, nothing else."
    )
    topic_covered: Optional[str] = Field(
        default=None,
        description="The specific interview topic this question targets, e.g. 'database indexing'. Null if this is a greeting-only message.",
    )
    is_follow_up: bool = Field(
        default=False,
        description="True if this message is a follow-up on the candidate's previous answer rather than a new topic.",
    )