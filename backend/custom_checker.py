# backend/analyzers/custom_checker.py

def check_custom_violations(log_data):
    custom_violations = []

    last_entry = None

    for entry in log_data:
        if last_entry:
            # Check 1: Odometer Decrease
            if entry.odometer < last_entry.odometer:
                custom_violations.append({
                    "violation": "Odometer rollback or incorrect log",
                    "details": f"Odometer decreased from {last_entry.odometer} to {entry.odometer} between {last_entry.time} and {entry.time} on {entry.date}."
                })

            # Check 2: Movement without Driving
            non_movement_statuses = ["Off Duty", "Sleeper", "On Duty"]
            if last_entry.status in non_movement_statuses:
                if (entry.odometer > last_entry.odometer) or (entry.location != last_entry.location):
                    if entry.status != "Driving":
                        custom_violations.append({
                            "violation": "Movement detected without Driving status",
                            "details": f"Movement from {last_entry.location} to {entry.location} detected between {last_entry.time} and {entry.time} on {entry.date}."
                        })

        last_entry = entry  # Move to next pair

    return custom_violations
