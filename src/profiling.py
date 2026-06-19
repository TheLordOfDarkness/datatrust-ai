def profile_dataset(df):

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns)
    }