from services.llm import LLMService
from prompts.evaluator_prompt import evaluator_prompt
from schemas.evaluator_schema import AnswerEvaluation
from utils.logger import logger


class EvaluateQuestion:
    def __init__(self):
        self.llm = LLMService()

    def evaluate(self, current_question, difficulty, answer) -> dict:

        logger.info(f"Evaluation started (difficulty={difficulty}, answer_length={len(answer)} chars)")

        if not answer or not answer.strip():
            logger.warning("Candidate skipped a question (empty answer)")


        prompt = evaluator_prompt(current_question, difficulty, answer)

        try:
            evaluation: AnswerEvaluation = self.llm.generate_response(prompt, schema=AnswerEvaluation)
        except Exception as e:
            logger.error(f"Evaluation failed (difficulty={difficulty}): {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"failed to evaluate answer: {e}",
                "data": None,
            }

        logger.info(f"Evaluation completed (score={evaluation.score}, next_action={evaluation.next_action})")

        return {
            "status": "success",
            "message": "answer evaluated",
            "data": evaluation.model_dump(),
        }