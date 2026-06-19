import pandas as pd

from quality_score import calculate_score
from checks.completeness import check_completeness
from checks.uniqueness import check_uniqueness
from checks.validity import check_email_validity
from report_generator import generate_html_report
from profiling import profile_dataset

df = pd.read_csv("data/sample.csv")
profile = profile_dataset(df)
completeness_results = check_completeness(df)
uniqueness_results = check_uniqueness(
    df,
    key_columns=["customer_id"]
)
email_validity_result = check_email_validity(
    df,
    column_name="email"
)
global_score = calculate_score(
    completeness_results,
    uniqueness_results,
    email_validity_result
)

print("\n====================")
print("DATA QUALITY REPORT")
print("====================")

print(f"\nGLOBAL SCORE : {global_score}/100\n")

print("COMPLETENESS")
for result in completeness_results:
    print(result)

print("\nUNIQUENESS")
for result in uniqueness_results:
    print(result)

print("\nEMAIL VALIDITY")
print(email_validity_result)

generate_html_report(
    global_score=global_score,
    completeness=completeness_results,
    uniqueness=uniqueness_results,
    email_validity=email_validity_result,
    profile=profile
)