from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import init_models
from deps import get_db
import schemas, crud

app = FastAPI(title="학사프로그램 API")

@app.on_event("startup")
async def on_startup():
    await init_models()

@app.get("/")
async def root():
    return {"msg": "TIS 학사 프로그램 API 입니다. /docs 로 이동하세요."}

@app.get("/health")
async def health():
    return {"ok": True}

# ----- Students CRUD -----
@app.post("/students", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
async def create_student(
    payload: schemas.StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    if payload.student_no:
        exists = await crud.get_student_by_no(db, payload.student_no)
        if exists:
            raise HTTPException(status_code=409, detail="student_no already exists")
    return await crud.create_student(db, payload)


@app.get("/students", response_model=List[schemas.StudentOut])
async def list_students(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_students(db, q, skip, limit)


@app.get("/students/{student_id}", response_model=schemas.StudentOut)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    s = await crud.get_student(db, student_id)
    if not s:
        raise HTTPException(status_code=404, detail="student not found")
    return s


@app.patch("/students/{student_id}", response_model=schemas.StudentOut)
async def update_student(
    student_id: int,
    payload: schemas.StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    s = await crud.get_student(db, student_id)
    if not s:
        raise HTTPException(status_code=404, detail="student not found")
    return await crud.update_student(db, s, payload)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    s = await crud.get_student(db, student_id)
    if not s:
        raise HTTPException(status_code=404, detail="student not found")
    await crud.delete_student(db, s)

