from schemas.schema import InterviewRequest, AnswerRequest
from fastapi import APIRouter
from agents.planner import InterviewPlanner
from agents.interviewer import Generate_Question
from agents.evaluator import EvaluateQuestion
from services.session_manager import SessionManagement
from utils.logger import logger

router = APIRouter(prefix="/interview")


@router.post("/start")
def start_interview(data: InterviewRequest):

    logger.info(f"/interview/start called (level={data.level})")

    #### 1 - plan the interview
    planner = InterviewPlanner()
    plan_result = planner.create_plan(
        resume=data.resume,
        job_discription=data.job_discription,
        level=data.level,
    )

    if plan_result["status"] == "error":
        logger.error(f"/interview/start failed at planning stage: {plan_result['message']}")
        return plan_result

    plan_data = plan_result["plan"]

    #### 2 - generate the first question
    interviewer = Generate_Question()
    question_result = interviewer.generate(
        candidate_summary=plan_data["candidate_summary"],
        interview_topics=plan_data["interview_topics"],
        difficulty=plan_data["difficulty"],
        conversation_history=None,
    )

    if question_result["status"] == "error":
        logger.error(f"/interview/start failed at question generation: {question_result['message']}")
        return question_result

    first_question = question_result["data"]  # dict: {message, topic_covered, is_follow_up}

    #### 3 - create the session
    manager = SessionManagement()
    session = manager.create_session(
        interview_plan=plan_data,
        first_question=first_question,
    )

    logger.info(f"/interview/start completed (session_id={session['session_id']})")
    return {
        "status": "success",
        "result": plan_result["message"],
        "session_id": session["session_id"],
        "question": first_question["message"],
    }


@router.post("/answer")
def get_answer(data: AnswerRequest):

    session_manager = SessionManagement()
    session = session_manager.get_session(data.session_id)

    if session.get("status") == "not found":
        return session

    ### 1
    current_question = session["current_question"]["message"]
    difficulty = session["interview_plan"]["difficulty"]

    ### 2 - evaluate the answer
    evaluator = EvaluateQuestion()
    evaluation_result = evaluator.evaluate(
        current_question=current_question,
        difficulty=difficulty,
        answer=data.answer,
    )

    if evaluation_result["status"] == "error":
        return evaluation_result

    evaluation = evaluation_result["data"]

    ### 3 - build conversation history text
    conversation_history = ""
    for turn in session["history"]:
        conversation_history += f"Interviewer: {turn['question']}\nCandidate: {turn['answer']}\n"

    ### 4 - generate the next question, following the Evaluator's decision
    interviewer = Generate_Question()
    next_question_result = interviewer.generate(
        candidate_summary=session["interview_plan"]["candidate_summary"],
        interview_topics=session["interview_plan"]["interview_topics"],
        difficulty=difficulty,
        conversation_history=conversation_history,
        next_action=evaluation["next_action"],
        previous_question=current_question,
        previous_answer=data.answer,
    )

    if next_question_result["status"] == "error":
        return next_question_result

    next_question = next_question_result["data"]  # dict

    ### 5 - update session
    session_manager.update_session(
        session_id=data.session_id,
        answer=data.answer,
        evaluation=evaluation,
        current_question=next_question,
    )

    return {
        "status": "success",
        "evaluation": evaluation,
        "next_question": next_question["message"],
    }

    