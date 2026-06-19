def calculate_score(
    completeness_results,
    uniqueness_results,
    validity_result
):

    score = 100.0

    # pénalité complétude
    for result in completeness_results:
        score -= result["missing_pct"] * 0.3

    # pénalité unicité
    for result in uniqueness_results:
        score -= result["duplicate_pct"] * 0.2

    # pénalité validité
    score -= validity_result["invalid_pct"] * 0.5

    return round(max(score, 0), 2)