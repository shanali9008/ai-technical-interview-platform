# AI Technical Interview Platform

An AI-powered technical interview system that plans an interview around a candidate's resume and a job description, conducts it turn by turn, evaluates each answer in real time, and produces a structured hiring report at the end.

> **Status: Work in progress.** This is an active learning/portfolio project, not a finished product currently improving.

---

## How it works

The system is built around four cooperating agents, each responsible for one stage of the interview lifecycle — similar to how a real hiring panel splits responsibilities:

| Agent | Role |
|---|---|
| **Planner** | Reads the resume + job description, identifies matching and missing skills, and produces an interview plan (topics, difficulty, candidate summary). |
| **Interviewer** | Generates one question at a time — either the next new topic, or a follow-up on the candidate's last answer — based on the plan and conversation so far. |
| **Evaluator** | Scores each answer (0–10), lists strengths/weaknesses, and decides whether the interview should follow up or move to a new topic. |
| **Report Generator** | Reviews the full transcript at the end and produces a final score, hire/borderline/no-hire decision, and specific, actionable recommendations. |

Every one of these agents calls an LLM (via [Groq](https://groq.com/) / LLaMA 3.3 70B through LangChain) and is **forced to return validated, structured output** using Pydantic schemas — the model can't return malformed or unpredictable data, because the response shape is enforced at the API boundary, not parsed from free text afterward.

### Request flow

```
POST /interview/start
  Client → Planner → Interviewer → Session created → first question returned

POST /interview/answer   (repeats per turn)
  Client → Evaluator (score + next_action) → Interviewer (follow-up or new topic)
         → Session updated → next question returned

GET /report/{session_id}
  Session (full transcript) → Report Generator → final hiring report
```

---

## Features

- **Resume input, two ways** — paste resume text directly, or upload a file (`.pdf`, `.docx`, `.txt`) and have it parsed automatically.
- **Structured, schema-enforced LLM output** — every agent response is validated against a Pydantic model (`InterviewPlan`, `InterviewerTurn`, `AnswerEvaluation`, `InterviewReport`), so downstream code always receives predictable data — no manual JSON parsing, no guessing at response shape.
- **Adaptive questioning** — the evaluator decides, after every answer, whether to dig deeper with a follow-up or move on to a new topic, based on how complete the answer was.
- **Session-based interviews** — each interview is tracked by a session ID, holding the interview plan, current question, and full conversation history.
- **Structured logging** — every meaningful step (plan created, question generated, evaluation completed, session updated, errors) is logged with timestamps and severity levels, so failures are traceable without needing to reproduce them.
- **Simple web UI** — a Streamlit frontend to run through an interview end-to-end: start form → live Q&A → final report, with color-coded interviewer/candidate chat bubbles.

---

## Tech stack

| Layer | Technology |
|---|---|
| API backend | FastAPI |
| LLM provider | Groq (LLaMA 3.3 70B) via `langchain-groq` |
| Structured output | Pydantic |
| Resume parsing | `pdfplumber` (PDF), `python-docx` (DOCX) |
| Frontend | Streamlit |
| Logging | Python's built-in `logging` module |

---

## Project structure

```
app/
├── main.py                      # FastAPI app entrypoint, router registration
│
├── routes/
│   ├── interview.py              # POST /interview/start, POST /interview/answer
│   ├── report.py                 # GET /report/{session_id}
│   └── resume.py                 # POST /resume/upload
│
├── agents/
│   ├── planner.py                 # InterviewPlanner
│   ├── interviewer.py             # Generate_Question
│   ├── evaluator.py               # EvaluateQuestion
│   └── report_generator.py        # ReportGenerator
│
├── prompts/
│   ├── prompt_planner.py
│   ├── prompt_interviewer.py
│   └── evaluator_prompt.py / report_prompt.py
│
├── schemas/
│   ├── planner_schema.py          # InterviewPlan
│   ├── interviewer_schema.py      # InterviewerTurn
│   ├── evaluator_schema.py        # AnswerEvaluation
│   └── report_schema.py           # InterviewReport
│
├── services/
│   ├── llm.py                     # LLMService — wraps ChatGroq + structured output
│   └── session_manager.py         # In-memory session store
│
├── utils/
│   ├── logger.py                  # Central "ai_recruiter" logger
│   └── resume_parser.py           # PDF/DOCX/TXT text extraction
│
└── schema.py                     # API request schemas (InterviewRequest, AnswerRequest)

app.py                            # Streamlit frontend
requirements.txt
```

---

## Getting started

### 1. Clone and install

```bash
git clone <your-repo-url>
cd AI_Recruiter
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_key_here
```

### 3. Run the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### 4. Run the frontend

In a separate terminal:

```bash
streamlit run frontend.py
```

---

## API overview

| Endpoint | Method | Description |
|---|---|---|
| `/interview/start` | `POST` | Submit resume, job description, and candidate level → returns a session ID and the first question. |
| `/interview/answer` | `POST` | Submit an answer for the current session → returns the evaluation and the next question. |
| `/report/{session_id}` | `GET` | Generate the final hiring report for a completed interview. |
| `/resume/upload` | `POST` | Upload a `.pdf`, `.docx`, or `.txt` resume file → returns extracted plain text. |

Full request/response schemas are available at `/docs` once the backend is running (FastAPI's auto-generated Swagger UI).

---

## Disclaimer

This is a personal learning and portfolio project exploring agentic LLM pipelines, structured output enforcement, and multi-stage evaluation systems. It is not production-hardened and should not be used as-is for real hiring decisions.