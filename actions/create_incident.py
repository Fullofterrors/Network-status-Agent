import json
import os
from datetime import datetime


def create_incident(problem_name, location, report_count):
    """
    Create a possible network incident.
    """

    incident = {
        "problem": problem_name,
        "location": location,
        "report_count": report_count,
        "status": "possible",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists("incidents.json"):
        with open("incidents.json", "r") as file:
            try:
                incidents = json.load(file)
            except json.JSONDecodeError:
                incidents = []
    else:
        incidents = []

    incidents.append(incident)

    with open("incidents.json", "w") as file:
        json.dump(incidents, file, indent=4)

    return {
        "success": True,
        "message": "Possible network incident created.",
        "incident": incident
    }