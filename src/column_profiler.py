import pandas as pd


def profile_columns(df: pd.DataFrame) -> list:
    profiles = []

    total_rows = len(df)

    for column in df.columns:
        series = df[column]

        profile = {
            "column": column,
            "dtype": str(series.dtype),
            "null_count": int(series.isna().sum()),
            "null_pct": float(round((series.isna().sum() / total_rows) * 100, 2)),
            "distinct_count": int(series.nunique(dropna=True)),
            "distinct_pct": float(round((series.nunique(dropna=True) / total_rows) * 100, 2)),
            "min": None,
            "max": None,
            "mean": None
        }

        if pd.api.types.is_numeric_dtype(series):
            profile["min"] = float(series.min()) if not series.dropna().empty else None
            profile["max"] = float(series.max()) if not series.dropna().empty else None
            profile["mean"] = float(round(series.mean(), 2)) if not series.dropna().empty else None

        profiles.append(profile)

    return profiles