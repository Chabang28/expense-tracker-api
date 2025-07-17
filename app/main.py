from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.database import database
from models import expenses

app = FastAPI()

class ExpenseIn(BaseModel):
    title: str
    amount: float
    category: str

class ExpenseOut(ExpenseIn):
    id: int

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/expenses/", response_model=ExpenseOut)
async def create_expense(expense: ExpenseIn):
    query = expenses.insert().values(**expense.dict())
    last_record_id = await database.execute(query)
    return {**expense.dict(), "id": last_record_id}

@app.get("/expenses/", response_model=List[ExpenseOut])
async def read_expenses():
    query = expenses.select()
    return await database.fetch_all(query)
