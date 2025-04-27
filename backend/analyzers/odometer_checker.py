from collections import defaultdict
from datetime import datetime
from backend.models.log_model import LogEntry  # Assuming you have a LogEntry or similar model

def analyze_odometer_timeline(log_entries: list[LogEntry]):
    """
    Analyzes odometer readings and returns a day-by-day timeline with anomalies.
    """
    days = defaultdict(list)

    # Sort entries by timestamp just in case
    log_entries.sort(key=lambda x: x.timestamp)

    previous = None
    for entry in log_entries:
        date_str = entry.timestamp.strftime("%Y-%m-%d")
        odometer = entry.odometer

        if previous:
            if odometer < previous.odometer:
                status = "anomaly_drop"
            elif odometer == previous.odometer and (entry.timestamp - previous.timestamp).seconds > 3600:
                status = "missing_data"
            else:
                status = "normal"
        else:
            status = "normal"

        days[date_str].append({
            "time": entry.timestamp.strftime("%H:%M"),
            "status": status
        })
        previous = entry

    # Transform into list sorted by date
    timeline = [{"date": date, "events": events} for date, events in sorted(days.items())]
    return timeline
