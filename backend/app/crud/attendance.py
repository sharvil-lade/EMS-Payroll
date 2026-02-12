from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, date
from app import models

def get_current_active_session(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.logout_time == None
    ).order_by(desc(models.Attendance.login_time)).first()

def check_in(db: Session, employee_id: int):
    today = datetime.now().date()
    
    active_session = get_current_active_session(db, employee_id)
    
    if active_session:
        raise ValueError("Employee is already checked in. Please check out first.")
    
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
    attendance = get_current_active_session(db, employee_id)
    
    if not attendance:
        raise ValueError("No active check-in record found. Please check in first.")
    
    attendance.logout_time = datetime.now()
    
    duration = attendance.logout_time - attendance.login_time
    total_hours = duration.total_seconds() / 3600
    attendance.total_hours = round(total_hours, 2)
    
    db.commit()
    db.refresh(attendance)
    return attendance


def get_attendance_report(db: Session, employee_id: int, start_date: date, end_date: date):
    records = db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.date >= start_date,
        models.Attendance.date <= end_date
    ).order_by(models.Attendance.date).all()
    
    total_hours = 0.0
    total_standard_hours = 0.0
    total_overtime_hours = 0.0
    daily_map = {}
    
    for record in records:
        d = record.date
        if d not in daily_map:
            daily_map[d] = {
                "sessions_count": 0, 
                "total_hours": 0.0,
                "standard_hours": 0.0,
                "overtime_hours": 0.0
            }
        
        daily_map[d]["sessions_count"] += 1
        if record.total_hours:
            daily_map[d]["total_hours"] += record.total_hours

    daily_breakdown = []
    for d, data in daily_map.items():
        day_total = data["total_hours"]
        day_of_week = d.weekday() # 0=Monday, 6=Sunday

        if day_of_week < 5: # Monday to Friday
            stand_h = min(day_total, 8.0)
            over_h = max(day_total - 8.0, 0.0)
        else: # Saturday and Sunday
            stand_h = 0.0
            over_h = 0.0
        
        data["standard_hours"] = round(stand_h, 2)
        data["overtime_hours"] = round(over_h, 2)
        data["total_hours"] = round(day_total, 2)

        total_hours += data["total_hours"]
        total_standard_hours += data["standard_hours"]
        total_overtime_hours += data["overtime_hours"]

        daily_breakdown.append({
            "date": d,
            "sessions_count": data["sessions_count"],
            "total_hours": data["total_hours"],
            "standard_hours": data["standard_hours"],
            "overtime_hours": data["overtime_hours"]
        })
    
    daily_breakdown.sort(key=lambda x: x["date"])

    return {
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_hours": round(total_hours, 2),
        "total_standard_hours": round(total_standard_hours, 2),
        "total_overtime_hours": round(total_overtime_hours, 2),
        "total_sessions": len(records),
        "daily_breakdown": daily_breakdown
    }
