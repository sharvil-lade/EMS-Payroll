from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    email: str
    department: str
    role: str
    hourly_rate: float
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    joining_date: date

    class Config:
        orm_mode = True
