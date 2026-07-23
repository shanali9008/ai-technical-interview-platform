import streamlit as st
import requests

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
API_BASE_URL = "http://127.0.0.1:8000"   # change if your FastAPI server runs elsewhere

st.set_page_config(page_title="AI Technical Interview Platform", page_icon="🧑‍💼", layout="centered")


# ----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of {"role": "interviewer"/"candidate", "text": "..."}
if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False
if "report" not in st.session_state:
    st.session_state.report = None


st.title("🧑‍💼 AI Technical Interview Platform")


# ----------------------------------------------------------------------------
# STEP 1 — START INTERVIEW FORM
# ----------------------------------------------------------------------------
if st.session_state.session_id is None:
    st.subheader("Start a new interview")

    with st.form("start_form"):
        level = st.selectbox("Candidate level", ["intern", "junior", "senior"])
        job_discription = st.text_area("Job description", height=120)

        st.markdown("**Resume** — upload a file, or paste the text below")
        resume_file = st.file_uploader("Upload resume (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
        resume_manual = st.text_area("...or paste resume text here", height=180)

        submitted = st.form_submit_button("Start Interview")

    if submitted:
        resume = resume_manual.strip()

        # If a file was uploaded, extract its text via the backend.
        # An uploaded file takes priority over manually typed text.
        if resume_file is not None:
            with st.spinner("Extracting text from resume..."):
                try:
                    files = {"file": (resume_file.name, resume_file.getvalue())}
                    upload_response = requests.post(f"{API_BASE_URL}/resume/upload", files=files)
                    upload_response.raise_for_status()
                    resume = upload_response.json()["resume_text"]
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not parse resume file: {e}")
                    resume = None

        if not job_discription.strip() or not resume:
            st.error("Please fill in the job description and either upload a resume or paste it manually.")
        else:
            with st.spinner("Analyzing candidate and preparing the first question..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/interview/start",
                        json={
                            "level": level,
                            "job_discription": job_discription,
                            "resume": resume,
                        },
                    )
                    response.raise_for_status()
                    data = response.json()

                    if data.get("status") == "error":
                        st.error(f"Failed to start interview: {data.get('message', 'unknown error')}")
                    else:
                        st.session_state.session_id = data["session_id"]
                        st.session_state.current_question = data["question"]
                        st.session_state.chat_history.append(
                            {"role": "interviewer", "text": data["question"]}
                        )
                        st.rerun()

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend: {e}")


# ----------------------------------------------------------------------------
# STEP 2 — INTERVIEW IN PROGRESS
# ----------------------------------------------------------------------------
elif not st.session_state.interview_finished:
    st.subheader("Interview in progress")

    # Render chat history
    # Render chat history
    for turn in st.session_state.chat_history:
        if turn["role"] == "interviewer":
            with st.chat_message("assistant", avatar="🧑‍💼"):
                st.markdown(turn["text"])
        else:
            with st.chat_message("user", avatar="🙋"):
                st.markdown(turn["text"])

    st.divider()

    with st.form("answer_form", clear_on_submit=True):
        answer = st.text_area("Your answer", height=120)
        col1, col2 = st.columns(2)
        submit_answer = col1.form_submit_button("Submit Answer")
        end_interview = col2.form_submit_button("End Interview & Get Report")

    if submit_answer:
        if not answer.strip():
            st.error("Please write an answer before submitting.")
        else:
            st.session_state.chat_history.append({"role": "candidate", "text": answer})

            with st.spinner("Evaluating your answer..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/interview/answer",
                        json={
                            "session_id": st.session_state.session_id,
                            "answer": answer,
                        },
                    )
                    response.raise_for_status()
                    data = response.json()

                    if data.get("status") == "error":
                        st.error(f"Failed to evaluate answer: {data.get('message', 'unknown error')}")
                    else:
                        next_question = data["next_question"]
                        st.session_state.current_question = next_question
                        st.session_state.chat_history.append(
                            {"role": "interviewer", "text": next_question}
                        )

                        # Optionally show the evaluation for transparency/debugging
                        with st.expander("See evaluation for this answer"):
                            st.json(data["evaluation"])

                        st.rerun()

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend: {e}")

    if end_interview:
        st.session_state.interview_finished = True
        st.rerun()


# ----------------------------------------------------------------------------
# STEP 3 — FINAL REPORT
# ----------------------------------------------------------------------------
else:
    st.subheader("Interview Report")

    if st.session_state.report is None:
        with st.spinner("Generating final report..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/report/{st.session_state.session_id}"
                )
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "error":
                    st.error(f"Failed to generate report: {data.get('message', 'unknown error')}")
                else:
                    st.session_state.report = data["report"]
            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach the backend: {e}")

    report = st.session_state.report
    if report:
        decision_color = {
            "Hire": "green",
            "Borderline": "orange",
            "No Hire": "red",
        }.get(report.get("decision"), "gray")

        st.metric("Interview Score", f"{report.get('interview_score', 0)} / 100")
        st.markdown(
            f"**Decision:** :{decision_color}[{report.get('decision', 'N/A')}]"
        )

        st.markdown("### Summary")
        st.write(report.get("summary", ""))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Strengths")
            for s in report.get("strengths", []):
                st.markdown(f"- {s}")
        with col2:
            st.markdown("### Weaknesses")
            for w in report.get("weaknesses", []):
                st.markdown(f"- {w}")

        st.markdown("### Recommendations")
        for r in report.get("recommendations", []):
            st.markdown(f"- {r}")

    st.divider()
    if st.button("Start a New Interview"):
        st.session_state.session_id = None
        st.session_state.current_question = None
        st.session_state.chat_history = []
        st.session_state.interview_finished = False
        st.session_state.report = None
        st.rerun()