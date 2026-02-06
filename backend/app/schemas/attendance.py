from pydantic import BaseModel
from typing import Optional
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
