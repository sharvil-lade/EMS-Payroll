from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from datetime import date
from io import StringIO
import csv
from app import crud, models, schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login/{employee_id}", response_model=schemas.AttendanceResponse)
def login_employee(employee_id: int, db: Session = Depends(get_db)):

    db_employee = crud.get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
        return crud.check_in(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout/{employee_id}", response_model=schemas.AttendanceResponse)
def logout_employee(employee_id: int, db: Session = Depends(get_db)):

    db_employee = crud.get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
        return crud.check_out(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/report", response_model=schemas.AttendanceReportResponse)
def get_attendance_report(
    employee_id: int, 
    start_date: date, 
    end_date: date, 
    db: Session = Depends(get_db)
):
    return crud.get_attendance_report(db, employee_id, start_date, end_date)


@router.post("/manual", response_model=schemas.ManualAttendanceResponse)
def create_manual_entry(manual_entry: schemas.ManualAttendanceCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, manual_entry.employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return crud.create_or_update_manual_attendance(db, manual_entry)


@router.post("/manual/upload")
async def batch_upload_manual_attendance(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    contents = await file.read()
    decoded_contents = contents.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(decoded_contents))
    
    success_count = 0
    errors = []
    
    for row in csv_reader:
        try:
            email = row.get("employee_email")
            date_str = row.get("date")
            std_hours_str = row.get("standard_hours")
            ot_hours_str = row.get("overtime_hours")
            
            if not all([email, date_str, std_hours_str, ot_hours_str]):
                raise ValueError(f"Missing required fields. Row: {row}")
                
            employee = db.query(models.Employee).filter(models.Employee.email == email).first()
            if not employee:
                raise ValueError(f"Employee with email {email} not found")
            
            try:
                attendance_date = date.fromisoformat(date_str)
            except ValueError:
                 raise ValueError("Invalid date format. Use YYYY-MM-DD")
            
            manual_entry = schemas.ManualAttendanceCreate(
                employee_id=employee.id,
                date=attendance_date,
                standard_hours=float(std_hours_str),
                overtime_hours=float(ot_hours_str)
            )
            
            crud.create_or_update_manual_attendance(db, manual_entry)
            success_count += 1

        except Exception as e:
            errors.append(f"Row error: {str(e)}")
            
    return {"message": "Upload processed", "success_count": success_count, "errors": errors}
