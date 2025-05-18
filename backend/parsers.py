# Assembling the corrected `parsers.py` with all final logic adjustments
import io
import re
import pdfplumber
from datetime import datetime
from backend.models import DriverLogEntry

DATETIME_RE = re.compile(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s*\d{2}:\d{2}:\d{2}")

PAGE_DATE_RE = re.compile(r"(\d{4})\s+-")
EXCLUDED_KEYWORDS = [
    "engine power-up", "engine shut-down", "certification", "diagnostic", "power data"
]

def extract_city_from_notes(notes: str) -> str:
    if "," in notes:
        parts = notes.strip().split(",")
        if len(parts) >= 2:
            return parts[-2].strip() + ", " + parts[-1].strip()
    return ""

def parse_log_block(lines, year) -> DriverLogEntry:
    full_text = " ".join(lines).replace("|", " ").strip()
    full_text = re.sub(r"\\s{2,}", " ", full_text)

    if any(keyword in full_text.lower() for keyword in EXCLUDED_KEYWORDS):
        return None

    result = {
        "timestamp": None,
        "status": None,
        "location": None,
        "odometer": None,
        "engine_hours": None,
        "origin": None,
        "notes": None,
        "raw_line": full_text,
        "unparsed": False,
        "fail_reason": [],
        "vehicle_id": "UNKNOWN"
    }

    try:
        ts_match = re.search(r"\b([A-Z][a-z]{2})\s+(\d{1,2}),\s*(\d{2}:\d{2}:\d{2})", full_text)

        ampm_match = re.search(r"\\b(am|pm|AM|PM)\\b", full_text)
        if ts_match:
            month, day, time_str = ts_match.groups()
            ampm = ampm_match.group(0).upper() if ampm_match else ("AM" if int(time_str.split(":")[0]) < 12 else "PM")
            dt = datetime.strptime(f"{month} {int(day)}, {year} {time_str} {ampm}", "%b %d, %Y %I:%M:%S %p")
            result["timestamp"] = dt.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            result["fail_reason"].append("Missing or malformed timestamp")
            result["unparsed"] = True

        origin_match = re.search(r"\b(Driver|Auto)\b", full_text)
        result["origin"] = origin_match.group(1) if origin_match else None

        statuses = ["Off Duty", "On Duty", "Sleeper", "Driving", "Intermediate", "Personal Use"]
        result["status"] = next((s for s in statuses if s in full_text), None)

        if not result["status"] and result["origin"] == "Auto" and "CLP" in full_text:
            result["status"] = "Intermediate w/ CLP"

        nums = re.findall(r"\d{5,6}(?:\.\d+)?", full_text)
        if len(nums) >= 2:
            result["odometer"] = int(float(nums[-2]))
            result["engine_hours"] = float(nums[-1])
        
        # Match base distance + direction + "from"
        base_loc = re.search(r"\b(\d{1,3}mi(?: [A-Z]{1,3})? from)\b", full_text)
        city_state = re.search(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)*,\s*[A-Z]{2})\b", full_text)
        if base_loc:
            result["location"] = base_loc.group(1)
             # Try to append city/state if it's not far from base match
            if city_state:
                result["location"] += " " + city_state.group(1)
        else:
            result["location"] = ""                 
        
        if result["origin"]:
            origin_pos = full_text.find(result["origin"])
            result["notes"] = full_text[origin_pos + len(result["origin"]):].strip(" ,")

        # Inference for Intermediate w/ CLP if status is missing
        if not result["status"] and result["origin"] == "Auto" and "CLP" in full_text:
            result["status"] = "Intermediate w/ CLP"

        if (result["status"] or "").lower() == "intermediate" and "CLP" in (result["notes"] or ""):
            result["status"] += " w/ CLP"

        # Simplify notes
        keywords = ["Delivery", "Pick up", "Break", "Sleeper", "PTI", "Fuel"]
        for word in keywords:
            if word.lower() in (result["notes"] or "").lower():
                result["notes"] = word
                break
        else:
            result["notes"] = ""

        # Location fix
        if not result["location"]:
            city = extract_city_from_notes(result["notes"] or "")
            if city:
                result["location"] = city
        else:
            result["location"] = re.sub(r"\b(?:AM|PM|am|pm)\b", "", result["location"])
            result["location"] = re.sub(r"([A-Za-z]) ([A-Z]{2})\b", r"\1, \2", result["location"]).strip()
            if not result["location"].startswith(" "):
                result["location"] = " " + result["location"]
            if not result["location"].endswith(" "):
                result["location"] += " "
        if result["location"].endswith("from") and result["notes"]:    
            if "," in result["notes"]:
                tail = result["notes"].split(",")[-2:]
                result["location"] += " " + ", ".join(t.strip() for t in tail)

        if not result["status"]:
            result["fail_reason"].append("Missing status")
            result["unparsed"] = True

        return DriverLogEntry(**result)

    except Exception as e:
        result["unparsed"] = True
        result["fail_reason"].append(f"Exception: {str(e)}")
        return DriverLogEntry(**result)

def parse_pdf_log(contents: bytes) -> list[DriverLogEntry]:
    unmatched = []
    parsed_entries = []
    seen = set()
    year = 2025

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        text_lines = []

        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.splitlines():
                if not year:
                    match = PAGE_DATE_RE.search(line)
                    if match:
                        year = int(match.group(1))

                if DATETIME_RE.match(line.strip()):
                    text_lines.append(line.strip())
                elif text_lines:
                    text_lines[-1] += " " + line.replace("\n", " ").strip()

        for line in text_lines:
            result = parse_log_block([line], year)
            if not result:
               unmatched.append(line)
               continue
            print(f"→ {result.timestamp} | {result.status} | {result.odometer} | {result.unparsed}")

            if not result.unparsed:
                key = (result.timestamp, result.status, result.odometer)
                if key not in seen:
                    seen.add(key)
                    parsed_entries.append(result)

            else:
                unmatched.append(result.raw_line)

    with open("unmatched_lines.txt", "w", encoding="utf-8") as f:
        for line in unmatched:
            f.write(f"{line}\\n")

    return parsed_entries




