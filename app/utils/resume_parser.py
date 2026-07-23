import io
import pdfplumber      # library for reading PDF files
import docx            # library for reading Word (.docx) files
from utils.logger import logger


def parse_resume(filename: str, file_bytes: bytes) -> str:
    """
    Takes an uploaded file and returns the plain text inside it.

    filename    -> e.g. "resume.pdf" (used to figure out the file type)
    file_bytes  -> the raw file content, uploaded by the user
    """

    logger.info(f"Parsing resume (filename={filename}, size={len(file_bytes)} bytes)")

    ##figure out what kind of file this is, from its name
    if filename.endswith(".pdf"):
        text = ""
        # pdfplumber opens the PDF and lets us read it page by page
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:                  # some pages might be blank/images
                    text += page_text + "\n"

    elif filename.endswith(".docx"):
        # docx.Document opens the Word file
        document = docx.Document(io.BytesIO(file_bytes))
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    elif filename.endswith(".txt"):
        # a .txt file is already plain text, just decode the raw bytes
        text = file_bytes.decode("utf-8")

    else:
        # anything else, we don't support yet
        logger.warning(f"Unsupported file type uploaded (filename={filename})")
        raise ValueError("Unsupported file type. Please upload a .pdf, .docx, or .txt file.")

    text =  text.strip()

    if not text:
        logger.warning(f"No text extracted from file (filename={filename})")
        raise ValueError("Could not find any text in this file. It may be a scanned image, not real text.")

    logger.info(f"Resume parsed successfully (filename={filename}, length={len(text)} chars)")

    return text