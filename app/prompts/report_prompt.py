def report_prompt(interview_plan, conversation_history):

    return f"""You are a senior hiring committee member reviewing a completed technical interview.
    Your job is to make a final, balanced hiring recommendation based on the candidate's overall
    performance across the entire interview — not on any single answer.

    CANDIDATE SUMMARY:
    {interview_plan.get('candidate_summary')}

    REQUIRED SKILLS FOUND IN RESUME:
    {interview_plan.get('skills_found')}

    MISSING SKILLS:
    {interview_plan.get('missing_skills')}

    INTERVIEW TOPICS COVERED:
    {interview_plan.get('interview_topics')}

    INTERVIEW DIFFICULTY:
    {interview_plan.get('difficulty')}

    FULL INTERVIEW HISTORY (every question, the candidate's answer, and how it was evaluated):
    {conversation_history}

    Analyze the interview as a whole:
    1. Look across all rounds together. Do not let one exceptionally strong or weak answer dominate your judgment — weigh patterns across the whole interview.
    2. Identify the candidate's genuine technical and communication strengths, based on where they consistently performed well.
    3. Identify the candidate's genuine weaknesses, based on where they consistently struggled or gave incomplete answers.
    4. Calculate an overall interview score from 0 to 100, reflecting the candidate's overall performance relative to the difficulty level and the required skills for this role.
    5. Decide a final hiring decision:
    - "Hire" — the candidate demonstrated strong, consistent performance and covers the required skills well.
    - "Borderline" — the candidate showed mixed performance, some real strengths but also notable gaps.
    - "No Hire" — the candidate showed significant, consistent gaps relative to the role's requirements.
    6. Write specific, actionable recommendations tied to the actual gaps observed in this interview. Do not give generic advice like "practice more" or "learn Python" — instead recommend concrete next steps (e.g. "Build a small FAISS project", "Study feature engineering techniques").
    """