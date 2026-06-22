import pandas as pd

from src.checks.completeness import check_completeness
from src.checks.uniqueness import check_uniqueness
from src.checks.validity import check_email_validity
from src.profiling import profile_dataset
from src.quality_score import calculate_score, quality_status
from src.recommendations import generate_recommendations
from src.schema_detector import detect_key_columns, detect_email_columns


def analyze_dataset(file_path: str) -> dict:
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

    return {
        "profile": profile,
        "completeness": completeness_results,
        "uniqueness": uniqueness_results,
        "email_validity": email_validity_result,
        "global_score": global_score,
        "status": status,
        "recommendations": recommendations,
        "detected_keys": key_columns,
        "detected_email_columns": email_columns
    }