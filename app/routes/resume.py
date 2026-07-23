from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.resume_parser import parse_resume
from utils.logger import logger

router = APIRouter(prefix="/resume")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    logger.info(f"/resume/upload called (filename={file.filename})")

    file_bytes = await file.read()

    try:
        resume_text = parse_resume(file.filename, file_bytes)
    except ValueError as e:
        # this is an error we expected and understand (bad file type, empty file)
        logger.warning(f"Resume upload rejected (filename={file.filename}): {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # this is something unexpected — a real bug or a library crash
        logger.error(f"Unexpected error parsing resume (filename={file.filename}): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong while processing your resume.")

    return {
        "filename": file.filename,
        "resume_text": resume_text
    }