from typing import List, Dict, Tuple
from backend.models import DriverLogEntry

def assign_vehicle_ids_by_odometer(
    logs: List[DriverLogEntry],
    daily_ranges: Dict[str, Dict[str, Tuple[int, int]]]
) -> List[DriverLogEntry]:
    for log in logs:
        day = log.timestamp.split(" ")[0]  # e.g., "2025-03-04"
        day_ranges = daily_ranges.get(day, {})
        matched = False

        for vehicle_id, (start, end) in day_ranges.items():
            if start <= log.odometer <= end:
                log.vehicle_id = vehicle_id
                matched = True
                break

        if not matched:
            log.vehicle_id = "UNKNOWN"

    return logs
