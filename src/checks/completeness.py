import pandas as pd

def check_completeness(df):
    results = []

    total_rows = len(df)

    for column in df.columns:

        missing_count = df[column].isnull().sum()

        missing_pct = round(
            (missing_count / total_rows) * 100,
            2
        )

        results.append({
            "column": column,
            "missing_count": int(missing_count),
            "missing_pct": float(missing_pct)
        })

    return results