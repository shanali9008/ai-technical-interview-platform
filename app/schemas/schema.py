from fastapi import File, UploadFile 
from pydantic import BaseModel, Field
from typing import  Literal


#--> Interview schema 
class InterviewRequest(BaseModel):

    level: Literal["intern", "junior", "senior"]
    job_discription: str = Field(...)
    resume: str = Field(...)


#--> Answer schema 
class AnswerRequest(BaseModel):

    session_id: str = Field(...)
    answer: str = Field(...)
        