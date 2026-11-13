from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

from actions.submit_report import submit_report
from agent.network_agent import process_report
from services.provider_service import change_incident_status

app = Flask(__name__)


def save_report(phone_number, problem_name, location):
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


def check_network_status(problem_name):
    if not os.path.exists("reports.json"):
        return 0

    with open("reports.json", "r") as file:
        try:
            reports = json.load(file)
        except json.JSONDecodeError:
            return 0

    count = 0

    for report in reports:
        if report["problem"] == problem_name:
            count += 1

    return count


@app.route("/", methods=["POST"])
@app.route("/ussd", methods=["POST"])
def ussd():

    session_id = request.form.get("sessionId")
    service_code = request.form.get("serviceCode")
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text", "")

    if text == "":
        response = """CON NETWORK ASSIST

1. Report network problem
2. Check network status
3. Troubleshoot
4. Help"""

    elif text == "1":
        response = """CON What problem are you experiencing?

1. No network
2. Slow internet
3. Calls dropping
4. SMS not working
5. Other"""

    elif text == "2":
        response = """CON NETWORK STATUS

1. Check my area
2. Recent reports"""

    elif text == "2*1":
        response = """CON CHECK MY AREA

This feature will use
network reports from
your area."""

    elif text == "2*2":

        no_network = check_network_status("No network")
        slow_internet = check_network_status("Slow internet")
        calls_dropping = check_network_status("Calls dropping")
        sms_not_working = check_network_status("SMS not working")

        response = f"""END RECENT REPORTS

No network: {no_network}
Slow internet: {slow_internet}
Calls dropping: {calls_dropping}
SMS not working: {sms_not_working}"""

    elif text == "3":
        response = """END TROUBLESHOOTING

Please restart your phone,
check your network settings,
and try again."""

    elif text == "4":
        response = """END NETWORK ASSIST

For network problems,
use option 1 to submit
a report."""

    elif text in ["1*1", "1*2", "1*3", "1*4", "1*5"]:

        response = """CON Where are you currently located?

1. Mombasa
2. Nairobi
3. Kisumu
4. Nakuru
5. Other"""

    elif text.startswith("1*") and len(text.split("*")) == 3:

        parts = text.split("*")

        problem = parts[1]
        location_option = parts[2]

        problems = {
            "1": "No network",
            "2": "Slow internet",
            "3": "Calls dropping",
            "4": "SMS not working",
            "5": "Other"
        }

        locations = {
            "1": "Mombasa",
            "2": "Nairobi",
            "3": "Kisumu",
            "4": "Nakuru",
            "5": "Other"
        }

        problem_name = problems.get(problem, "Other")
        location = locations.get(location_option, "Other")

        submit_report(
            phone_number,
            problem_name,
            location
        )

        agent_result = process_report(
            problem_name,
            location
        )

        response = "END " + agent_result["user_message"]

    else:
        response = "END Invalid option. Please try again."

    return response

@app.route("/api/provider/incidents/status", methods=["POST"])
def provider_incident_status():
    # Read the API key from the Authorization header.
    authorization = request.headers.get("Authorization", "")
    scheme, separator, api_key = authorization.partition(" ")

    if (
        not separator
        or scheme.lower() != "bearer"
        or not api_key.strip()
    ):
        return jsonify({
            "success": False,
            "message": "Unauthorized: valid provider credentials are required."
        }), 401

    # Require a JSON request body.
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "A valid JSON request body is required."
        }), 400

    location = data.get("location")
    problem_name = data.get("problem")
    new_status = data.get("status")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (location, problem_name, new_status)
    ):
        return jsonify({
            "success": False,
            "message": "location, problem, and status are required."
        }), 400

    result = change_incident_status(
        location.strip(),
        problem_name.strip(),
        new_status.strip(),
        api_key=api_key.strip()
    )

    if not result["success"]:
        if result["message"].startswith("Unauthorized:"):
            return jsonify(result), 401

        return jsonify(result), 400

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)