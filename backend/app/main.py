from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import employees, attendance, payroll
from app.core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Attendance & Payroll System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(payroll.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Employee Attendance & Payroll System API (Modularized)"}
