from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class AttendanceBase(BaseModel):
    employee_id: int

class AttendanceLog(AttendanceBase):
    pass

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    login_time: Optional[datetime] = None
    logout_time: Optional[datetime] = None
    total_hours: float

    class Config:
        orm_mode = True

class AttendanceReportResponse(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    total_hours: float
    total_standard_hours: float
    total_overtime_hours: float
    total_sessions: int
    daily_breakdown: List[dict]

class ManualAttendanceCreate(BaseModel):
    employee_id: int
    date: date
    standard_hours: float
    overtime_hours: float

class ManualAttendanceResponse(ManualAttendanceCreate):
    id: int
    
    class Config:
        orm_mode = True
