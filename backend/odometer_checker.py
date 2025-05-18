from collections import defaultdict
from datetime import datetime
from backend.models import DriverLogEntry
  # Assuming you have a LogEntry or similar model

def analyze_odometer_timeline(log_entries: list[DriverLogEntry]):
    
    days = defaultdict(list)

    # Sort entries by timestamp just in case
    log_entries.sort(key=lambda x: x.timestamp)

    previous = None
    for entry in log_entries:
        timestamp_obj = datetime.strptime(entry.timestamp, "%Y-%m-%d %H:%M")
        date_str = timestamp_obj.strftime("%Y-%m-%d")
        if date_str not in days:
            days[date_str] = []
        odometer = entry.odometer

        if previous:
            previous_timestamp_obj = datetime.strptime(previous.timestamp, "%Y-%m-%d %H:%M")
            if odometer < previous.odometer:
                status = "anomaly_drop"
            elif odometer == previous.odometer and (timestamp_obj - previous_timestamp_obj).seconds > 3600:
                status = "missing_data"
            else:
                status = "normal"
        else:
            status = "normal"

        days[date_str].append({
            "time": entry.timestamp.strftime("%H:%M"),
            "status": status,
            "location": entry.location,   # <-- add location
            "odometer": entry.odometer    # <-- add odometer value
        })
        previous = entry

    # Transform into list sorted by date
    timeline = [{"date": date, "events": events} for date, events in sorted(days.items())]
    return timeline
