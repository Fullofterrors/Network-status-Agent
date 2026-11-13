import json
import os


def get_recent_reports(limit=10):
    """
    Get the most recent network reports.
    """

    if not os.path.exists("reports.json"):
        return []

    with open("reports.json", "r") as file:
        try:
            reports = json.load(file)
        except json.JSONDecodeError:
            return []

    # Return the most recent reports first
    return reports[-limit:]

def get_reports_by_location(location):
    """
    Get reports from a specific location.
    """

    reports = get_recent_reports(limit=1000)

    location_reports = []

    for report in reports:
        if report.get("location") == location:
            location_reports.append(report)

    return location_reports

def get_report_history(problem_name=None, location=None):
    """
    Get historical network reports.
    
    Can filter by problem, location, or both.
    """

    reports = get_recent_reports(limit=1000)

    history = []

    for report in reports:

        if problem_name is not None:
            if report.get("problem") != problem_name:
                continue

        if location is not None:
            if report.get("location") != location:
                continue

        history.append(report)

    return history

def check_network_status(problem_name):
    """
    Count how many reports exist for a specific network problem.
    """

    reports = get_recent_reports(limit=1000)

    count = 0

    for report in reports:
        if report.get("problem") == problem_name:
            count += 1

    return count

def get_active_incidents():
    """
    Get incidents that are still active.
    """

    if not os.path.exists("incidents.json"):
        return []

    with open("incidents.json", "r") as file:
        try:
            incidents = json.load(file)
        except json.JSONDecodeError:
            return []

    active_incidents = []

    for incident in incidents:
        status = incident.get("status")

        if status in ["possible", "investigating"]:
            active_incidents.append(incident)

    return active_incidents