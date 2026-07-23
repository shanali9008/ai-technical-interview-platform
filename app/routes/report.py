from fastapi import APIRouter
from services.session_manager import SessionManagement
from agents.report_generator import ReportGenerator

router = APIRouter(prefix="/report")


@router.get("/{session_id}")
def get_report(session_id: str):

    session_manager = SessionManagement()
    session = session_manager.get_session(session_id)

    if session.get("status") == "not found":
        return session

    report_generator = ReportGenerator()
    report_result = report_generator.generate_report(
        interview_plan=session["interview_plan"],
        conversation_history=session["history"],
    )

    if report_result["status"] == "error":
        return report_result

    return {
        "status": "success",
        "session_id": session_id,
        "report": report_result["data"],
    }