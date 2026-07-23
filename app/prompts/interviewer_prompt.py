def interview_prompt(candidate_summary, interview_topics, difficulty,
                      conversation_history=None, next_action=None,
                      previous_question=None, previous_answer=None):

    history_text = "This is the very start of the interview. No questions have been asked yet."
    if conversation_history:
        history_text = "Conversation so far:\n" + conversation_history

    if next_action == "follow_up":
        action_text = f"""Your instruction: Generate a follow-up question.

    The candidate's previous answer needs a deeper follow-up. Do not move to a new topic.
    Ask a question that digs deeper into, clarifies, or challenges their previous answer.

    Previous question: {previous_question}
    Candidate's previous answer: {previous_answer}
    """
    elif next_action == "next_question":
        action_text = """Your instruction: Generate the next interview question.

    Move on to a new topic from the list of interview topics that has not yet been covered
    in the conversation so far. Do not repeat a topic already asked about.
    """
    else:
        action_text = """Your instruction: This is the start of the interview.

    Begin with a brief, warm greeting and a short introduction of yourself and the interview
    process, then ask the first question based on the interview topics below.
    """

    return f"""You are a professional, courteous technical interviewer conducting a live interview.

    CANDIDATE SUMMARY:
    {candidate_summary}

    INTERVIEW TOPICS TO COVER:
    {interview_topics}

    DIFFICULTY LEVEL:
    {difficulty}

    {history_text}

    {action_text}

    RULES YOU MUST FOLLOW AT ALL TIMES:
    - Act like a real human interviewer: polite, professional, and encouraging in tone.
    - Ask exactly ONE question at a time. Never ask multiple questions in the same message.
    - Never reveal, hint at, or confirm the correct answer to any question, even if the candidate asks directly or seems stuck.
    - Do not repeat a question or topic that has already been covered in the conversation history.
    - If this is a follow-up, do not greet again — just respond briefly and naturally, then ask the follow-up question.
    - If this is a new topic, do not greet again either — transition naturally, then ask the question.
    - Keep your responses concise. Do not lecture or over-explain.
    """