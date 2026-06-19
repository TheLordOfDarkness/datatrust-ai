def generate_recommendations(
    global_score,
    completeness,
    uniqueness,
    email_validity
):
    recommendations = []

    if global_score < 80:
        recommendations.append(
            "Overall data quality score is below 80. A remediation plan should be prioritized."
        )

    for item in completeness:
        if item["missing_pct"] > 0:
            recommendations.append(
                f"Column '{item['column']}' contains {item['missing_pct']}% missing values."
            )

    for item in uniqueness:
        if item["duplicate_pct"] > 0:
            recommendations.append(
                f"Column '{item['column']}' contains {item['duplicate_pct']}% duplicate values."
            )

    if email_validity["invalid_pct"] > 0:
        recommendations.append(
            f"Column '{email_validity['column']}' contains {email_validity['invalid_pct']}% invalid email values."
        )

    return recommendations