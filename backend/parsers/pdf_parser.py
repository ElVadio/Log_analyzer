import pdfplumber
from io import BytesIO
from models.log_model import DriverLogEntry
import re

def parse_driver_log(file_content: bytes):
    entries = []
    with pdfplumber.open(BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                # Dummy regex parsing; needs adjustment per real log format
                match = re.match(r"(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+(Off Duty|Sleeper|On Duty|Driving)\s+(\d+)\s+(.+)", line)
                if match:
                    date, time, status, odometer, location = match.groups()
                    entry = DriverLogEntry(
                        date=date,
                        time=time,
                        status=status,
                        odometer=int(odometer),
                        location=location.strip()
                    )
                    entries.append(entry)
    return entries