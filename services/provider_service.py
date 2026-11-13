
from actions.update_incident_status import update_incident_status
from services.provider_auth import authenticate_provider


def change_incident_status(
    location,
    problem_name,
    new_status,
    api_key=None
):
    """
    Request an incident status change.

    Authenticate the provider before attempting
    to update an incident.
    """

    if not authenticate_provider(api_key):
        return {
            "success": False,
            "message": (
                "Unauthorized: valid provider "
                "credentials are required."
            )
        }

    return update_incident_status(
        location,
        problem_name,
        new_status
    )