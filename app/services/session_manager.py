import uuid
from utils.logger import logger

sessions = {}


class SessionManagement:

    def create_session(self, interview_plan, first_question):
        session_id = str(uuid.uuid4())

        sessions[session_id] = {
            "session_id": session_id,
            "interview_plan": interview_plan,
            "current_question": first_question,
            "current_question_number": 1,
            "history": [],
            "completed": False,
        }

        logger.info(f"Session created (session_id={session_id})")
        return sessions[session_id]

    def get_session(self, session_id):
        session = sessions.get(session_id)

        if session is None:
            logger.warning(f"Session not found (session_id={session_id})")
            return {
                "status": "not found",
                "message": f"session not found for session_id: {session_id}",
            }

        logger.info(f"Session retrieved (session_id={session_id})")
        return session

    def update_session(self, session_id, answer, current_question=None, evaluation=None):
        session = sessions.get(session_id)
        if session is None:
            logger.warning(f"Session update failed — not found (session_id={session_id})")
            return {
                "status": "not found",
                "message": f"session not found for session_id: {session_id}",
            }

        # The question being answered right now is whatever was stored as
        # "current_question" BEFORE we overwrite it with the next one.
        answered_question = session["current_question"]
        answered_question_text = (
            answered_question["message"] if isinstance(answered_question, dict) else answered_question
        )

        if evaluation is not None:
            session["history"].append({
                "question": answered_question_text,
                "answer": answer,
                "evaluation": evaluation,
            })

        if current_question is not None:
            session["current_question"] = current_question
            session["current_question_number"] += 1

        logger.info(f"Session updated (session_id={session_id}, question_number={session['current_question_number']})")
        return session

        