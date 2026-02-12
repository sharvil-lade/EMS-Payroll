from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app import models, schemas
from .employee import get_employee

def calculate_payroll(db: Session, employee_id: int, start_date: date, end_date: date):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.date >= start_date,
        models.Attendance.date <= end_date
    ).all()

    overtime_rate = employee.overtime_rate if employee.overtime_rate else 0.0

    total_standard_hours = 0.0
    total_overtime_hours = 0.0
    total_hours = 0.0

    for record in attendance_records:
        day_of_week = record.date.weekday()
        
        if day_of_week < 5:
            daily_hours = record.total_hours
            if daily_hours > 8:
                daily_standard = 8.0
                daily_extra = daily_hours - 8.0
            else:
                daily_standard = daily_hours
                daily_extra = 0.0
            
            total_standard_hours += daily_standard
            total_overtime_hours += daily_extra
            total_hours += daily_hours
        else:
            pass

    standard_pay = total_standard_hours * employee.hourly_rate
    overtime_pay = total_overtime_hours * overtime_rate
    total_pay = standard_pay + overtime_pay
    
    return schemas.SalaryReportResponse(
        employee_id=employee.id,
        employee_name=employee.name,
        start_date=start_date,
        end_date=end_date,
        total_hours=round(total_hours, 2),
        total_standard_hours=round(total_standard_hours, 2),
        total_overtime_hours=round(total_overtime_hours, 2),
        hourly_rate=employee.hourly_rate,
        overtime_rate=overtime_rate,
        standard_pay=round(standard_pay, 2),
        overtime_pay=round(overtime_pay, 2),
        total_pay=round(total_pay, 2)
    )
