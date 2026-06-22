def detect_key_columns(df):
    key_columns = []

    key_patterns = [
        "id",
        "_id",
        "code",
        "number",
        "num"
    ]

    for column in df.columns:
        column_lower = column.lower()

        if any(pattern in column_lower for pattern in key_patterns):
            key_columns.append(column)

    return key_columns


def detect_email_columns(df):
    email_columns = []

    for column in df.columns:
        column_lower = column.lower()

        if "email" in column_lower or "mail" in column_lower:
            email_columns.append(column)

    return email_columns