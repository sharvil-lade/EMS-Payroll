from sqlalchemy.orm import Session
from app import models, schemas

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def create_employee_bulk(db: Session, employees: list[schemas.EmployeeCreate]):
    db_employees = [models.Employee(**employee.dict()) for employee in employees]
    db.add_all(db_employees)
    db.commit()
    for emp in db_employees:
        db.refresh(emp)
    return db_employees

def update_employee(db: Session, employee_id: int, employee_update: schemas.EmployeeCreate):

    db_employee = get_employee(db, employee_id)
    if db_employee:
        for key, value in employee_update.dict().items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
