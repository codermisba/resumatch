from fastapi import FastAPI, UploadFile, Form
from .resume_parser import extract_resume_text
from .jd_parser import extract_jd_text
from database import save_result, get_results
from relevance import compute_relevance

app = FastAPI(title="Automated Resume Relevance Checker")

# ---------------------------
# POST /analyze
# ---------------------------
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile, 
    jd: UploadFile, 
    job_id: str = Form(...), 
    candidate: str = Form(...)
):
    """
    Analyze a resume against a job description.
    Hard-coded keywords can be extracted dynamically from JD later.
    """

    # 1️⃣ Extract text from uploaded files
    resume_text = extract_resume_text(await resume.read(), resume.filename)
    jd_text = extract_jd_text(await jd.read(), jd.filename)
    
    # 2️⃣ Hard-coded keywords (can replace with dynamic extraction from JD)
    keywords = ["AWS", "FastAPI", "Python", "Docker", "Machine Learning", "Kubernetes", "PostgreSQL"]
    
    # 3️⃣ Compute relevance (returns score 0-100, verdict, missing keywords, feedback)
    score, verdict, missing, feedback = compute_relevance(resume_text, jd_text, keywords, job_id)
    
    # 4️⃣ Prepare result object
    result = {
        "candidate": candidate,
        "job_id": job_id,
        "score": score,
        "verdict": verdict,
        "missing": missing,
        "feedback": feedback
    }

    # 5️⃣ Save to database
    save_result(result)

    # 6️⃣ Return JSON
    return result

# ---------------------------
# GET /results/{job_id}
# ---------------------------
@app.get("/results/{job_id}")
def fetch_results(job_id: str):
    """
    Fetch all analyzed resumes for a given job_id
    """
    return get_results(job_id)
