from pydantic import BaseModel
from datetime import date
from typing import List

class AttendanceSession(BaseModel):
    date: date
    sessions_count: int
    total_hours: float
    standard_hours: float
    overtime_hours: float

    class Config:
        from_attributes = True

class AttendanceReportResponse(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    total_hours: float
    total_standard_hours: float
    total_overtime_hours: float
    total_sessions: int
    daily_breakdown: List[AttendanceSession]

class PayrollReportResponse(BaseModel):
    employee_id: int
    employee_name: str
    start_date: date
    end_date: date
    total_hours: float
    hourly_rate: float
    total_pay: float
