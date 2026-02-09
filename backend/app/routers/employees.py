from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io

from app import crud, schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@router.post("/upload-csv", response_model=List[schemas.EmployeeResponse])
async def upload_employees_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = await file.read()
    stream = io.StringIO(content.decode("utf-8"))
    csv_reader = csv.DictReader(stream)
    
    employees_data = []
    for row in csv_reader:
        try:
            employee_data = schemas.EmployeeCreate(
                name=row["name"],
                email=row["email"],
                department=row["department"],
                role=row["role"],
                hourly_rate=float(row["hourly_rate"])
            )
            employees_data.append(employee_data)
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV: {e}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid data format: {e}")

    return crud.create_employee_bulk(db=db, employees=employees_data)

@router.get("/", response_model=List[schemas.EmployeeResponse])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{employee_id}", response_model=schemas.EmployeeResponse)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
