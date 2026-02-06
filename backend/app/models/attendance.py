from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, default=datetime.now().date)
    login_time = Column(DateTime, nullable=True)
    logout_time = Column(DateTime, nullable=True)
    total_hours = Column(Float, default=0.0)

    employee = relationship("Employee", back_populates="attendance_records")
