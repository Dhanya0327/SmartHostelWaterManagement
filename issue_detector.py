def detect_issues(
    total_usage,
    room_limit,
    shower_duration,
    wash_duration
):
    issues = []

    if total_usage > room_limit:
        issues.append("High Water Consumption")

    if shower_duration > 30:
        issues.append("Long Shower Usage")

    if wash_duration > 4:
        issues.append("Possible Tap Left Open")

    return issues