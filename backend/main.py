# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.parsers.parsers import parse_driver_log
from analyzers.hos_checker import check_hos_violations
from analyzers.custom_checker import check_custom_violations
from backend.analyzers.odometer_checker import analyze_odometer_timeline
from backend.parsers.parsers import load_logs  # or wherever load PDF logs
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/odometer-timeline")
async def get_odometer_timeline():
    logs = load_logs()  # Implement to load and parse your pdf logs
    timeline = analyze_odometer_timeline(logs)
    return timeline

app = FastAPI()

@app.post("/upload-log/")
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()

    try:
        log_data = parse_driver_log(content)
        hos_violations = check_hos_violations(log_data)
        custom_violations = check_custom_violations(log_data)

        return {
            "log_data": [entry.dict() for entry in log_data],
            "hos_violations": hos_violations,
            "custom_violations": custom_violations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
