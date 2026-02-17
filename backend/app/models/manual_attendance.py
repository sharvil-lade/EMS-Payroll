from sqlalchemy import Column, Integer, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class ManualAttendance(Base):
    __tablename__ = "manual_attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, index=True)
    standard_hours = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)

    employee = relationship("Employee")

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_employee_date'),
    )
