import pandas as pd

from checks.completeness import check_completeness

df = pd.read_csv("data/sample.csv")

results = check_completeness(df)

print("\n=== COMPLETENESS REPORT ===\n")

for result in results:
    print(result)