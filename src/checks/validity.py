import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def check_email_validity(df, column_name):
    invalid_count = 0
    total_rows = len(df)

    for value in df[column_name]:
        if value is None:
            continue

        value = str(value).strip()

        if value == "" or value.lower() == "nan":
            continue

        if not re.match(EMAIL_REGEX, value):
            invalid_count += 1

    invalid_pct = float(
        round((invalid_count / total_rows) * 100, 2)
    )

    return {
        "column": column_name,
        "invalid_count": invalid_count,
        "invalid_pct": invalid_pct
    }