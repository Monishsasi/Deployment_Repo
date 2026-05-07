from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import HTTPException
import os
from dotenv import load_dotenv

from nodes.parsing import DocumentExtractor
from agent import ResumeAnalyzerAgent

app = FastAPI()

load_dotenv(override=True)

#  CORS (Get data from React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent once
resume_analyzer = ResumeAnalyzerAgent()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Analyzer API"}


@app.post("/analyze-resume/")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None)
):
    try:
        # RESUME PROCESSING
        if not resume:
            return {"error": "Resume file is required"}

        resume_bytes = await resume.read()

        extractor = DocumentExtractor(resume_bytes, resume.filename)
        resume_text = extractor.extract()

        # JD PROCESSING
        if jd_file:
            jd_bytes = await jd_file.read()
            jd_extractor = DocumentExtractor(jd_bytes, jd_file.filename)
            jd_final_text = jd_extractor.extract()

        elif jd_text:
            jd_final_text = jd_text

        else:
            return {"error": "Provide either jd_file or jd_text"}

        # ANALYSIS
        result = resume_analyzer.run(resume_text, jd_final_text)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
    )