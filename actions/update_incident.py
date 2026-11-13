
import json
import os
from datetime import datetime


ACTIVE_STATUSES = {"possible", "investigating"}


def update_incident(location, problem_name, report_count, status=None):
    """
    Update the report count of an active network incident.

    Official status changes are handled separately.
    The status parameter is retained for compatibility, but
    status changes through this function are not permitted.
    """

    if status is not None:
        return {
            "success": False,
            "message": (
                "Status changes are not permitted through "
                "update_incident(). Use the authorized "
                "provider status workflow."
            )
        }

    if not os.path.exists("incidents.json"):
        return {
            "success": False,
            "message": "No incidents found."
        }

    with open("incidents.json", "r") as file:
        try:
            incidents = json.load(file)
        except json.JSONDecodeError:
            incidents = []

    if not isinstance(incidents, list):
        return {
            "success": False,
            "message": "Incident data has an invalid format."
        }

    for incident in incidents:
        if (
            incident.get("location") == location
            and incident.get("problem") == problem_name
            and incident.get("status") in ACTIVE_STATUSES
        ):
            incident["report_count"] = report_count
            incident["updated_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            with open("incidents.json", "w") as file:
                json.dump(incidents, file, indent=4)

            return {
                "success": True,
                "message": "Incident report count updated successfully.",
                "incident": incident
            }

    return {
        "success": False,
        "message": "Matching active incident not found."
    }