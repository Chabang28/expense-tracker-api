from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redirect root "/" to API docs
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Pydantic schemas
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    description: str | None = None

class ExpenseOut(ExpenseCreate):
    id: int

    class Config:
        orm_mode = True

@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model=List[ExpenseOut])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, updated_expense: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in updated_expense.dict().items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense

@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
