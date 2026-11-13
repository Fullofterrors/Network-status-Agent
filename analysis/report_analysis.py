from datetime import datetime, timedelta

def classify_report(report_text):
    """
    Classify a user's network problem.
    """

    text = report_text.lower()

    # No network
    if (
        "no network" in text
        or "no signal" in text
        or "no service" in text
        or "network unavailable" in text
    ):
        return "No network"

    # Slow internet
    elif (
        "slow internet" in text
        or "internet slow" in text
        or "internet is slow" in text
        or "internet is very slow" in text
        or "data is slow" in text
        or "data is very slow" in text
    ):
        return "Slow internet"

    # Calls dropping
    elif (
        "call dropping" in text
        or "calls dropping" in text
        or "call keeps dropping" in text
        or "calls keep dropping" in text
        or "calls are dropping" in text
    ):
        return "Calls dropping"

    # SMS problems
    elif (
        "sms" in text
        or "text message" in text
        or "messages not sending" in text
        or "message not sending" in text
    ):
        return "SMS not working"

    # Unknown problem
    else:
        return "Other"

def troubleshoot_device(problem_name):
    """
    Provide basic troubleshooting steps for a network problem.
    """

    if problem_name == "No network":
        return [
            "Restart your phone.",
            "Make sure Airplane Mode is off.",
            "Check that the SIM card is inserted correctly.",
            "Check your mobile network settings.",
            "Try manual network selection."
        ]

    elif problem_name == "Slow internet":
        return [
            "Restart your phone.",
            "Make sure mobile data is enabled.",
            "Check your network settings.",
            "Move to an area with better signal.",
            "Try again after a few minutes."
        ]

    elif problem_name == "Calls dropping":
        return [
            "Restart your phone.",
            "Check your signal strength.",
            "Make sure Airplane Mode is off.",
            "Check your SIM and network settings.",
            "Try making the call from another location."
        ]

    elif problem_name == "SMS not working":
        return [
            "Restart your phone.",
            "Check your signal strength.",
            "Check that the SIM card is active.",
            "Check your message settings.",
            "Try sending the SMS again."
        ]

    else:
        return [
            "Restart your phone.",
            "Check your network settings.",
            "Check your signal strength.",
            "Try again."
        ]


def analyze_network_pattern(
    reports,
    minimum_reports=3,
    time_window_minutes=30
):
    """
    Detect a possible network problem using recent reports.
    """

    if not reports:
        return {
            "significant": False,
            "reason": "No reports available."
        }

    # Get the current time
    now = datetime.now()

    # Define the time limit
    time_limit = now - timedelta(
        minutes=time_window_minutes
    )

    # Count recent reports for each problem and location
    patterns = {}

    for report in reports:
        timestamp_text = report.get("timestamp")

        if not timestamp_text:
            continue

        try:
            report_time = datetime.strptime(
                timestamp_text,
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            continue

        # Ignore reports older than the time window
        if report_time < time_limit or report_time > now:
            continue

        problem = report.get("problem", "Other")
        location = report.get("location", "Unknown")

        key = (problem, location)

        if key not in patterns:
            patterns[key] = 0

        patterns[key] += 1

    # Look for a significant recent pattern
    for key, count in patterns.items():

        if count >= minimum_reports:
            problem, location = key

            return {
                "significant": True,
                "problem": problem,
                "location": location,
                "report_count": count,
                "time_window_minutes": time_window_minutes,
                "reason": (
                    f"{count} reports of '{problem}' "
                    f"were received from {location} "
                    f"within the last "
                    f"{time_window_minutes} minutes."
                )
            }

    return {
        "significant": False,
        "reason": (
            "No unusual recent report pattern detected "
            f"within the last {time_window_minutes} minutes."
        )
    }

def generate_incident_summary(pattern):
    """
    Generate a simple summary for a possible network incident.
    """

    if not pattern.get("significant"):
        return "No possible network incident detected."

    problem = pattern.get("problem", "Unknown")
    location = pattern.get("location", "Unknown")
    report_count = pattern.get("report_count", 0)

    summary = f"""POSSIBLE NETWORK INCIDENT

Location: {location}
Problem: {problem}
Reports: {report_count}

Summary:
Multiple reports of '{problem}' were received
from {location}. The pattern may require
further investigation by the network provider."""

    return summary