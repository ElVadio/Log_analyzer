# backend/mileage_analyzer.py

def detect_odometer_anomalies_with_vehicle_change(events, vehicles):
    """
    Detect odometer anomalies, considering vehicle changes.
    
    Args:
        events (list): List of event dicts (each must contain 'odometer', 'timestamp', 'location', 'notes').
        vehicles (list): List of vehicles assigned for the day.

    Returns:
        list: List of anomaly dicts.
    """
    anomalies = []
    last_odometer = None

    for idx, event in enumerate(events):
        if event.get('odometer') is None:
            continue

        if last_odometer is not None and event['odometer'] < last_odometer:
            vehicle_swapped = False

            if len(vehicles) > 1:
                notes = event.get('notes', '').lower()
                previous_notes = events[idx-1].get('notes', '').lower() if idx > 0 else ''

                if 'chance truck' in notes or 'chance truck' in previous_notes:
                    vehicle_swapped = True

            if not vehicle_swapped:
                anomalies.append({
                    "timestamp": event.get('timestamp'),
                    "last_odometer": last_odometer,
                    "current_odometer": event.get('odometer'),
                    "location": event.get('location')
                })

        last_odometer = event['odometer']

    return anomalies
