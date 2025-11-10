from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_student(db: AsyncSession, student_id: int) -> Optional[models.Student]:
    result = await db.execute(
        select(models.Student).where(models.Student.id == student_id)
    )
    return result.scalar_one_or_none()


async def get_student_by_no(db: AsyncSession, student_no: str) -> Optional[models.Student]:
    result = await db.execute(
        select(models.Student).where(models.Student.student_no == student_no)
    )
    return result.scalar_one_or_none()


async def list_students(
    db: AsyncSession,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Student]:
    stmt = select(models.Student).offset(skip).limit(limit).order_by(models.Student.id.desc())
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            (models.Student.name.ilike(like)) |
            (models.Student.student_no.ilike(like)) |
            (models.Student.edu_no.ilike(like))
        )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_student(
    db: AsyncSession,
    payload: schemas.StudentCreate,
) -> models.Student:
    obj = models.Student(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def update_student(
    db: AsyncSession,
    db_obj: models.Student,
    payload: schemas.StudentUpdate,
) -> models.Student:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_obj, key, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_student(db: AsyncSession, db_obj: models.Student) -> None:
    await db.delete(db_obj)
    await db.commit()
