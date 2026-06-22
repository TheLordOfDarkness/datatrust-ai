import os

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.services.analysis_service import analyze_dataset
from src.report_generator import generate_html_report


app = FastAPI(
    title="DataTrust AI",
    description="AI-powered Data Quality Platform",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={}
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_file(
    request: Request,
    file: UploadFile = File(...)
):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    analysis = analyze_dataset(file_path)

    generate_html_report(
        global_score=analysis["global_score"],
        completeness=analysis["completeness"],
        uniqueness=analysis["uniqueness"],
        email_validity=analysis["email_validity"],
        profile=analysis["profile"],
        recommendations=analysis["recommendations"],
        status=analysis["status"],
        column_profiles=analysis["column_profiles"]
    )

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "global_score": analysis["global_score"],
            "completeness": analysis["completeness"],
            "uniqueness": analysis["uniqueness"],
            "email_validity": analysis["email_validity"],
            "profile": analysis["profile"],
            "recommendations": analysis["recommendations"],
            "status": analysis["status"],
            "column_profiles": analysis["column_profiles"]
        }
    )


@app.post("/api/analyze")
async def analyze_file_api(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    analysis = analyze_dataset(file_path)

    return analysis