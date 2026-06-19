def check_uniqueness(df, key_columns):

    results = []

    total_rows = len(df)

    for column in key_columns:

        duplicate_count = (
            df[column]
            .duplicated()
            .sum()
        )

        duplicate_pct = float(
            round(
                duplicate_count /
                total_rows * 100,
                2
            )
        )

        results.append({
            "column": column,
            "duplicate_count": int(duplicate_count),
            "duplicate_pct": float(duplicate_pct)
        })

    return results