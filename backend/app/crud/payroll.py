from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app import models, schemas
from .employee import get_employee

def calculate_payroll(db: Session, employee_id: int, start_date: date, end_date: date):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    
    total_hours = db.query(func.sum(models.Attendance.total_hours)).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.date >= start_date,
        models.Attendance.date <= end_date
    ).scalar() or 0.0
    
    total_pay = total_hours * employee.hourly_rate
    
    return schemas.SalaryReportResponse(
        employee_id=employee.id,
        employee_name=employee.name,
        start_date=start_date,
        end_date=end_date,
        total_hours=total_hours,
        hourly_rate=employee.hourly_rate,
        total_pay=total_pay
    )
