from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Type, TypeVar

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class LLMService:
    def __init__(self, model: str = "llama-3.3-70b-versatile", temperature: float = 0):
        self.chatmodel = ChatGroq(model=model, temperature=temperature)

    def generate_response(self, prompt: str, schema: Type[T]) -> T:
        """
        Calls the LLM and forces its output to conform to `schema`.
        Every agent file should pass its own Pydantic model here.
        """
        structured_llm = self.chatmodel.with_structured_output(schema)
        return structured_llm.invoke(prompt)