from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    student_no: Optional[str] = None
    edu_no: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    student_no: Optional[str] = None
    edu_no: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class StudentOut(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 객체 → Pydantic 변환
