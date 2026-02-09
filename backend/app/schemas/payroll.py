from pydantic import BaseModel
from typing import Optional
from datetime import date

class SalaryReportRequest(BaseModel):
    employee_id: Optional[int] = None
    start_date: date
    end_date: date

class SalaryReportResponse(BaseModel):
    employee_id: int
    employee_name: str
    start_date: date
    end_date: date
    total_hours: float
    total_standard_hours: float
    total_extra_hours: float
    hourly_rate: float
    total_pay: float
