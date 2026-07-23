from services.llm import LLMService
from prompts.planner_prompt import planner_prompt
from schemas.planner_schema import InterviewPlan
from utils.logger import logger

class InterviewPlanner:
    def __init__(self):
        self.llm = LLMService()

    def create_plan(self, resume: str, job_discription: str, level: str) -> dict:

        logger.info(f"Interview planning started (level={level}, resume_length={len(resume)} chars, jd_length={len(job_discription)} chars)")

        prompt = planner_prompt(resume, level, job_discription)

        try:
            plan: InterviewPlan = self.llm.generate_response(prompt, schema=InterviewPlan)
        except Exception as e:
            logger.error(f"Interview plan generation failed (level={level}): {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"failed to create interview plan: {e}",
                "data": None,
            }

        logger.info(f"Interview plan generated successfully (topics={len(plan.interview_topics)}, difficulty={plan.difficulty})")

        return {
            "status": "success",
            "message": f"interview plan created for {level}",
            "data": {
                "resume": resume,
                "job_discription": job_discription,
            },
            "plan": plan.model_dump(),
        }