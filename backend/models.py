from dataclasses import dataclass, field
from typing import Optional, List
from pydantic import BaseModel 

@dataclass
class DriverLogEntry:
    timestamp: Optional[str]
    status: Optional[str]
    location: Optional[str]
    odometer: Optional[int]
    engine_hours: Optional[float]
    origin: Optional[str]
    notes: Optional[str]
    raw_line: str
    unparsed: bool
    fail_reason: List[str]
    vehicle_id: str = field(default="UNKNOWN")

class Violation(BaseModel):
    violation: str
    details: str
