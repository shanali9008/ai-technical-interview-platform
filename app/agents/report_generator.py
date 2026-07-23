from services.llm import LLMService
from prompts.report_prompt import report_prompt
from schemas.report_schema import InterviewReport
from utils.logger import logger


class ReportGenerator:
    def __init__(self):
        self.llm = LLMService()

    def generate_report(self, interview_plan=None, conversation_history=None) -> dict:

        logger.info("Report generation started")

        if not interview_plan or not conversation_history:
            return {
                "status": "error",
                "message": "interview_plan and conversation_history are required to generate a report",
                "data": None,
            }

        prompt = report_prompt(interview_plan=interview_plan, conversation_history=conversation_history)

        try:
            report: InterviewReport = self.llm.generate_response(prompt, schema=InterviewReport)
        except Exception as e:
            logger.error(f"Report generation failed: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"failed to generate interview report: {e}",
                "data": None,
            }

        logger.info(f"Report generated successfully (decision={report.decision}, score={report.interview_score})")


        return {
            "status": "success",
            "message": "interview report generated",
            "data": report.model_dump(),
        }

        