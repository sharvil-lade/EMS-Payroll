from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    role = Column(String)
    joining_date = Column(Date, default=datetime.now().date)
    hourly_rate = Column(Float)
    overtime_rate = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)

    attendance_records = relationship("Attendance", back_populates="employee")
