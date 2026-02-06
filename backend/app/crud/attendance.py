from sqlalchemy.orm import Session
from datetime import datetime, date
from app import models

def get_active_attendance(db: Session, employee_id: int, today: date):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.date == today
    ).first()

def check_in(db: Session, employee_id: int):
    today = datetime.now().date()
    existing_attendance = get_active_attendance(db, employee_id, today)
    
    if existing_attendance:
        raise ValueError("Attendance already exists for today.")
    
    new_attendance = models.Attendance(
        employee_id=employee_id,
        date=today,
        login_time=datetime.now()
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def check_out(db: Session, employee_id: int):
    today = datetime.now().date()
    attendance = get_active_attendance(db, employee_id, today)
    
    if not attendance:
        raise ValueError("No check-in record found for today.")
    
    if attendance.logout_time:
        raise ValueError("Already checked out for today.")
    
    attendance.logout_time = datetime.now()
    
    # Calculate duration
    duration = attendance.logout_time - attendance.login_time
    total_hours = duration.total_seconds() / 3600 # Convert to hours
    attendance.total_hours = round(total_hours, 2)
    
    db.commit()
    db.refresh(attendance)
    return attendance
