import os
import pandas as pd

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.checks.completeness import check_completeness
from src.checks.uniqueness import check_uniqueness
from src.checks.validity import check_email_validity
from src.profiling import profile_dataset
from src.quality_score import calculate_score, quality_status
from src.recommendations import generate_recommendations
from src.report_generator import generate_html_report
from src.schema_detector import detect_key_columns, detect_email_columns


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

    df = pd.read_csv(file_path)

    profile = profile_dataset(df)

    completeness_results = check_completeness(df)

    key_columns = detect_key_columns(df)

    uniqueness_results = check_uniqueness(
        df,
        key_columns=key_columns
    )

    email_columns = detect_email_columns(df)

    if email_columns:
        email_validity_result = check_email_validity(
            df,
            column_name=email_columns[0]
        )
    else:
        email_validity_result = {
            "column": "N/A",
            "invalid_count": 0,
            "invalid_pct": 0.0
        }

    global_score = calculate_score(
        completeness_results,
        uniqueness_results,
        email_validity_result
    )

    status = quality_status(global_score)

    recommendations = generate_recommendations(
        global_score,
        completeness_results,
        uniqueness_results,
        email_validity_result
    )

    generate_html_report(
        global_score=global_score,
        completeness=completeness_results,
        uniqueness=uniqueness_results,
        email_validity=email_validity_result,
        profile=profile,
        recommendations=recommendations,
        status=status
    )

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "global_score": global_score,
            "completeness": completeness_results,
            "uniqueness": uniqueness_results,
            "email_validity": email_validity_result,
            "profile": profile,
            "recommendations": recommendations,
            "status": status
        }
    )