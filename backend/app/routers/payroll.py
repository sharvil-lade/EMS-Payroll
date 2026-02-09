from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/payroll",
    tags=["payroll"],
    responses={404: {"description": "Not found"}},
)

@router.post("/report", response_model=schemas.SalaryReportResponse)
def get_payroll_report(report_request: schemas.SalaryReportRequest, db: Session = Depends(get_db)):
    report = crud.calculate_payroll(db, report_request.employee_id, report_request.start_date, report_request.end_date)
    if not report:
        raise HTTPException(status_code=404, detail="Employee not found or no data")
    return report
