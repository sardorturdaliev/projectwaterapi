from fastapi import HTTPException
from functions.kassa_func import update_kassa_minus
from models.kassa import Kassas
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.expenses import Expenses
from datetime import datetime


def all_expenses(search, page, limit, db, branch_id):
    expenses = db.query(Expenses)
    if branch_id > 0:
        expenses = expenses.filter(Expenses.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Expenses.name.like(search_formatted))
    else:
        search_filter = Expenses.id > 0
    expenses = expenses.filter(search_filter).order_by(Expenses.name.asc())
    return pagination(expenses, page, limit)


def create_expenses_y(form, db, this_user):
    kassa = the_one(form.kassa_id, Kassas, db)
    if form.sorce in ['user', 'warehouses']:
        raise HTTPException(status_code=400, detail="source error")
    if form.money <= kassa.balance:
        new_expenses_db = Expenses(
            money=form.money,
            date=datetime.today(),
            user_id=this_user.id,
            branch_id=this_user.branch_id,
            source=form.source,
            source_id=form.source_id,
            kassa_id=form.kassa_id,
            comment=form.kassa_id,
        )
        save_in_db(db, new_expenses_db)
        update_kassa_minus(form.kassa_id, form.money, db, this_user.id)
    else:
        raise HTTPException(status_code=400,detail="Kassada buncha pul mavjud emas!!!")


def update_expenses_y(form, db, this_user):
    if the_one(form.id, Expenses, db):
        old_expenses = the_one(form.id, Expenses, db)
        new_expense_money = old_expenses.money + form.money
        kassa = the_one(old_expenses.kassa_id, Kassas, db)
        if form.sorce in ['user', 'warehouses']:
            raise HTTPException(status_code=400, detail="source error")
        if form.money <= kassa.balance:
            db.query(Expenses).filter(Expenses.id == form.id).update({
                Expenses.id: form.id,
                Expenses.money: new_expense_money,
                Expenses.comment: form.comment,
                Expenses.user_id: this_user.id
            })
            db.commit()
            update_kassa_minus(old_expenses.kassa_id, form.money, db, this_user.id)
        else:
            raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud bas")

