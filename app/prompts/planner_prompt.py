def planner_prompt(resume: str, level: str, job_discription: str) -> str:
    return f"""You are a senior technical recruiter and interview panel lead with 10+ years of experience hiring for engineering roles.

Your task is to analyze a candidate and design an interview plan before any questions are asked.

CANDIDATE LEVEL: {level}

RESUME:
{resume}

JOB DESCRIPTION:
{job_discription}

Think through this analysis step by step internally:
1. Extract the key technical and soft skills required by the job description.
2. Extract the skills, tools, and experience actually present in the resume.
3. Compare the two lists to find overlapping skills (skills_found) and required skills that are missing or weak (missing_skills).
4. Based on the gaps and strengths, decide which specific topics the interview should cover to properly evaluate this candidate for this role.
5. Set a difficulty level that matches the candidate's stated level ({level}) — intern should be fundamentals-focused, junior should test applied knowledge, senior should probe depth, tradeoffs, and system-level thinking.
6. Write a 2-3 sentence summary of the candidate's fit for this role.

Do not leave any field empty — if something genuinely cannot be determined, use "unknown" or an empty list, not a placeholder sentence.
"""