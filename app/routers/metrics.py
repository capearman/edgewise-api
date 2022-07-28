from fastapi import APIRouter, status, Response, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, metrics_class, oauth2
import json

router = APIRouter(
    prefix="/metrics",
    tags=['Metrics'],
)

@router.get("/", response_model=schemas.Metrics)
def get_metrics(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    planned_expenses_query = db.query(func.sum(models.Category.planned)).filter(models.Category.type == 'Expense', models.Category.owner_id == current_user.id).first()
    planned_expenses = planned_expenses_query[0]
    if planned_expenses == None:
        planned_expenses = 0

    planned_income_query = db.query(func.sum(models.Category.planned)).filter(models.Category.type == 'Income', models.Category.owner_id == current_user.id).first()
    planned_income = planned_income_query[0]
    if planned_income == None:
        planned_income = 0

    actual_income_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == 'Income', models.Transaction.owner_id == current_user.id).first()
    actual_income = actual_income_query[0]
    if actual_income == None:
        actual_income = 0

    actual_expenses_query = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == 'Expense', models.Transaction.owner_id == current_user.id).first()
    actual_expenses = actual_expenses_query[0]
    if actual_expenses == None:
        actual_expenses = 0

    last_month_balance = db.query(models.User.last_month_balance).filter(models.User.id == current_user.id).first()

    print(last_month_balance[0])

    metrics_obj = metrics_class.Metrics(actual_income, planned_income, actual_expenses, planned_expenses, last_month_balance[0])

    metrics = {
        "money_to_categorize": float(metrics_obj.get_money_to_categorize()),
        "current_balance": float(metrics_obj.get_current_balance())
    }

    print(f"\n\nmetrics: {metrics}\n\n")
    return metrics
