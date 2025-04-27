def detect_odometer_anomalies_with_vehicle_change(events, vehicles):
    anomalies = []
    last_odometer = None
    current_vehicle_index = 0

    for idx, event in enumerate(events):
        if event.get('odometer') is None:
            continue
        
        if last_odometer is not None and event['odometer'] < last_odometer:
            # Potential anomaly detected
            vehicle_swapped = False

            if len(vehicles) > 1:
                # Check nearby events if there was a truck change note
                notes = event.get('notes', '').lower()
                previous_notes = events[idx - 1].get('notes', '').lower() if idx > 0 else ''

                if 'chance truck' in notes or 'chance truck' in previous_notes:
                    vehicle_swapped = True

            if not vehicle_swapped:
                anomalies.append({
                    "timestamp": event['timestamp'],
                    "last_odometer": last_odometer,
                    "current_odometer": event['odometer'],
                    "location": event.get('location')
                })
            # If swapped, no anomaly

        last_odometer = event['odometer']
    
    return anomalies
