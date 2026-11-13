import json
import os
from datetime import datetime


def submit_report(phone_number, problem_name, location):
    """
    Submit and save a network problem report.
    """

    report = {
        "phone": phone_number,
        "problem": problem_name,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists("reports.json"):
        with open("reports.json", "r") as file:
            try:
                reports = json.load(file)
            except json.JSONDecodeError:
                reports = []
    else:
        reports = []

    reports.append(report)

    with open("reports.json", "w") as file:
        json.dump(reports, file, indent=4)

    return {
        "success": True,
        "message": "Report submitted successfully.",
        "report": report
    }