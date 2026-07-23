from prompts.interviewer_prompt import interview_prompt
from services.llm import LLMService
from schemas.interviewer_schema import InterviewerTurn
from utils.logger import logger


class Generate_Question:
    def __init__(self):
        self.llm = LLMService()

    def generate(self, candidate_summary, interview_topics, difficulty,
                 conversation_history=None, next_action=None,
                 previous_question=None, previous_answer=None) -> dict:

        logger.info(f"Question generation started (next_action={next_action}, difficulty={difficulty})")         

        prompt = interview_prompt(
            candidate_summary,
            interview_topics,
            difficulty,
            conversation_history=conversation_history,
            next_action=next_action,
            previous_question=previous_question,
            previous_answer=previous_answer,
        )

        try:
            turn: InterviewerTurn = self.llm.generate_response(prompt, schema=InterviewerTurn)
        except Exception as e:
            logger.error(f"Question generation failed (next_action={next_action}): {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"failed to generate interview question: {e}",
                "data": None,
            }

        logger.info(f"Question generated successfully (topic={turn.topic_covered}, follow_up={turn.is_follow_up})")

        return {
            "status": "success",
            "message": "question generated",
            "data": turn.model_dump(),
        }