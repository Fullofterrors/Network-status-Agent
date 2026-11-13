
import json
import os
from datetime import datetime


INCIDENTS_FILE = "incidents.json"

ALLOWED_TRANSITIONS = {
    "possible": ["investigating"],
    "investigating": ["resolved"],
    "resolved": ["closed"],
    "closed": []
}


def update_incident_status(location, problem_name, new_status):
    """
    Update an incident's status through the provider workflow.

    Call this function only after the provider's identity
    and permissions have been verified by the application.
    """

    if new_status not in ALLOWED_TRANSITIONS:
        return {
            "success": False,
            "message": "Invalid incident status."
        }

    if not os.path.exists(INCIDENTS_FILE):
        return {
            "success": False,
            "message": "No incidents found."
        }

    with open(INCIDENTS_FILE, "r") as file:
        try:
            incidents = json.load(file)
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "Incident data is invalid."
            }

    if not isinstance(incidents, list):
        return {
            "success": False,
            "message": "Incident data has an invalid format."
        }

    for incident in incidents:
        if (
            incident.get("location") == location
            and incident.get("problem") == problem_name
        ):
            current_status = incident.get("status")

            if current_status not in ALLOWED_TRANSITIONS:
                return {
                    "success": False,
                    "message": "Current incident status is invalid."
                }

            if new_status not in ALLOWED_TRANSITIONS[current_status]:
                return {
                    "success": False,
                    "message": (
                        f"Transition from '{current_status}' "
                        f"to '{new_status}' is not allowed."
                    )
                }

            incident["status"] = new_status
            incident["updated_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            with open(INCIDENTS_FILE, "w") as file:
                json.dump(incidents, file, indent=4)

            return {
                "success": True,
                "message": "Incident status updated successfully.",
                "incident": incident
            }

    return {
        "success": False,
        "message": "Matching incident not found."
    }