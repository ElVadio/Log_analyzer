from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.parsers import parse_pdf_log
from backend.utils.odometer_extractor import extract_odometer_ranges_by_day
from backend.utils.vehicle_assignment import assign_vehicle_ids_by_odometer
import os

app = FastAPI(title="Driver Log Analyzer")

# Allowed status codes to include in output
ALLOWED_STATUSES = {"Driving", "On Duty", "Off Duty", "Sleeper", "Personal Use", "Intermediate w/ CLP"}


@app.post("/api/parse")
async def parse_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Only PDF uploads are accepted")

    try:
        contents = await file.read()

        # Step 1: Parse raw log entries from PDF
        logs = parse_pdf_log(contents)
        print("Parsed statuses:", [entry.status for entry in logs])


        # Step 2: Extract odometer-to-vehicle ID mapping
        ranges_by_day = extract_odometer_ranges_by_day(contents)

        # Step 3: Assign vehicle ID based on odometer ranges
        logs = assign_vehicle_ids_by_odometer(logs, ranges_by_day)

        # Step 4: Load unmatched lines for debug
        unmatched = []
        if os.path.exists("unmatched_lines.txt"):
            with open("unmatched_lines.txt", "r", encoding="utf-8") as f:
                unmatched = f.read().splitlines()

        # Step 5: Filter logs by status
        filtered = [
            {
                "vehicle_id": e.vehicle_id,
                "timestamp": e.timestamp,
                "status": e.status,
                "odometer": e.odometer,
                "location": e.location,
                "engine_hours": e.engine_hours,
                "origin": e.origin,
                "notes": e.notes
            }
            for e in logs
            if e.status in ALLOWED_STATUSES
        ]

        # Step 6: Return result
        if not filtered:
            return {"detail": "No matching log entries found", "unmatched_lines": unmatched}

        return {
            "entries": filtered,
            "unmatched_lines": unmatched,
            "odometer_ranges": ranges_by_day
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing PDF: {str(e)}")
