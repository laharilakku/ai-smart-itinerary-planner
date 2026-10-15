from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import Expense, Trip
from app.schemas.schemas import ExpenseCreate, ExpenseOut, ExpenseSummary
from app.services.currency_service import convert_to_inr, build_expense_summary, get_supported_currencies

router = APIRouter()


@router.post("/", response_model=ExpenseOut, status_code=201)
async def add_expense(data: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    amount_inr = convert_to_inr(data.amount, data.currency)
    expense = Expense(**data.model_dump(), amount_inr=amount_inr)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.get("/trip/{trip_id}", response_model=List[ExpenseOut])
async def list_expenses(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Expense).where(Expense.trip_id == trip_id).order_by(Expense.date.desc())
    )
    return result.scalars().all()


@router.get("/trip/{trip_id}/summary", response_model=ExpenseSummary)
async def expense_summary(trip_id: int, db: AsyncSession = Depends(get_db)):
    trip_result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = trip_result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    exp_result = await db.execute(select(Expense).where(Expense.trip_id == trip_id))
    expenses = exp_result.scalars().all()

    budget_inr = convert_to_inr(trip.total_budget or 0.0, trip.currency or "INR")
    summary = build_expense_summary(expenses, budget_inr)

    return ExpenseSummary(trip_id=trip_id, **summary)


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense).where(Expense.id == expense_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    await db.delete(exp)
    await db.commit()


@router.get("/currencies")
async def supported_currencies():
    return {"currencies": get_supported_currencies()}
