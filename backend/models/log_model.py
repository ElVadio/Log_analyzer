from pydantic import BaseModel

class DriverLogEntry(BaseModel):
    date: str
    time: str
    status: str
    odometer: int
    location: str

class Violation(BaseModel):
    violation: str
    details: str
