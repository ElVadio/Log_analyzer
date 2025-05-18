import io
import re
from typing import Dict, Tuple
import pdfplumber
from datetime import datetime

DATE_RE = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}")
VEHICLE_BLOCK_RE = re.compile(r"(\d{3,6})\s+[A-Z0-9]{17}\s+(\d{5,6})\s*[-–]\s*(\d{5,6})")

def extract_odometer_ranges_by_day(pdf_bytes: bytes) -> Dict[str, Dict[str, Tuple[int, int]]]:
    """
    Extract odometer ranges grouped by date from all pages.
    Returns: { "2025-03-04": { "394382": (434490, 435916) }, ... }
    """
    ranges_by_day: Dict[str, Dict[str, Tuple[int, int]]] = {}
    current_day = None

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            date_match = DATE_RE.search(text)
            if date_match:
                date_str = date_match.group(0)
                current_day = datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")

            if not current_day:
                continue  # skip if no date is found

            if current_day not in ranges_by_day:
                ranges_by_day[current_day] = {}

            for match in VEHICLE_BLOCK_RE.findall(text):
                vehicle_id, odo_start, odo_end = match
                ranges_by_day[current_day][vehicle_id] = (int(odo_start), int(odo_end))

    return ranges_by_day
