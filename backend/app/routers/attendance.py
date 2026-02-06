from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login/{employee_id}", response_model=schemas.AttendanceResponse)
def login_employee(employee_id: int, db: Session = Depends(get_db)):
    # Verify employee exists
    db_employee = crud.get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
        return crud.check_in(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout/{employee_id}", response_model=schemas.AttendanceResponse)
def logout_employee(employee_id: int, db: Session = Depends(get_db)):
     # Verify employee exists
    db_employee = crud.get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
         return crud.check_out(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
