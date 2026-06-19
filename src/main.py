import pandas as pd

from checks.completeness import check_completeness
from checks.uniqueness import check_uniqueness
from checks.validity import check_email_validity

df = pd.read_csv("data/sample.csv")

completeness_results = check_completeness(df)
uniqueness_results = check_uniqueness(
    df,
    key_columns=["customer_id"]
)
email_validity_result = check_email_validity(
    df,
    column_name="email"
)

print("\n====================")
print("DATA QUALITY REPORT")
print("====================\n")

print("COMPLETENESS")
for result in completeness_results:
    print(result)

print("\nUNIQUENESS")
for result in uniqueness_results:
    print(result)

print("\nEMAIL VALIDITY")
print(email_validity_result)