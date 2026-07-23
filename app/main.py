from fastapi import FastAPI
from routes.interview import router as interview_router
from routes.resume import router as resume_router
from routes.report import router as  report_router


app = FastAPI(
    title = "AI Technical Interview Platform--API",
    version="1.0.0"
    )

app.include_router(interview_router)
app.include_router(resume_router)
app.include_router(report_router)


@app.get('/')
def status():

    return {
        "message":"Api is running"
        }


