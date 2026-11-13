from analysis.report_analysis import (
    classify_report,
    troubleshoot_device,
    analyze_network_pattern,
    generate_incident_summary
)

from tools.report_tools import (
    get_recent_reports,
    get_reports_by_location,
    get_report_history,
    check_network_status,
    get_active_incidents
)

from actions.create_incident import create_incident
from actions.update_incident import update_incident
from textwrap import dedent


def process_report(report_text, location):
    """
    Process an already-submitted network report.
    """

    user_message = ""

    # Step 1: Classify the problem
    problem = classify_report(report_text)

    print("Problem classified as:", problem)

    # Step 2: Provide basic troubleshooting
    troubleshooting = troubleshoot_device(problem)

    print("\nTroubleshooting steps:")
    for step in troubleshooting:
        print("-", step)

    # Step 3: Get reports from the same location
    reports = get_reports_by_location(location)

    print("\nReports from location:")
    print(reports)

    # Step 4: Analyze the network pattern
    pattern = analyze_network_pattern(reports)

    print("\nPattern analysis:")
    print(pattern)

    # Step 5: Check if a significant pattern was detected
    if pattern.get("significant"):

        # Generate a summary
        summary = generate_incident_summary(pattern)

        user_message = dedent(f"""\
            NETWORK ASSIST

            Your report has been recorded.

            Several similar reports have been
            received from {location}.

            The issue may require investigation
            by the network provider.
        """)

        print("\nIncident summary:")
        print(summary)

        # Step 6: Check for existing active incidents
        active_incidents = get_active_incidents()

        matching_incident = None

        for incident in active_incidents:

            if (
                incident.get("problem") == problem
                and incident.get("location") == location
            ):
                matching_incident = incident
                break

        # Step 7: Update existing incident
        if matching_incident:

            result = update_incident(
                location,
                problem,
                pattern.get("report_count", 0)
            )

        # Step 8: Create new incident
        else:

            result = create_incident(
                problem,
                location,
                pattern.get("report_count", 0)
            )

        print("\nIncident action:")
        print(result)

    else:

        user_message = dedent("""\
            NETWORK ASSIST

            Your report has been recorded.

            No unusual network pattern has
            been detected yet. Thank you for
            helping us monitor network problems.
        """)

        print("\nNo significant network pattern detected.")

    return {
        "problem": problem,
        "troubleshooting": troubleshooting,
        "pattern": pattern,
        "user_message": user_message
    }