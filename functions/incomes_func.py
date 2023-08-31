from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException
from functions.kassa_func import update_kassa_r
from models.incomes import Incomes
from models.kassa import Kassas
from models.orders import Orders
from models.trades import Trades
from models.transfers import Transfers
from models.users import Users
from models.warehouse_products import Warehouses_products
from utils.db_operations import get_in_db, save_in_db, the_one
from utils.paginatsiya import pagination


def all_income_r(page, limit, db, branch_id):
    income = db.query(Incomes)
    if branch_id > 0:
        income = income.filter(Incomes.branch_id == branch_id)

    income = income.order_by(Incomes.id.desc())
    return pagination(income, page, limit)


def create_income_r(form, db, thisuser):
    kassa = the_one(form.kassa_id, Kassas, db)
    if form.source == "order":
        order = db.query(Orders).filter(Orders.id == form.source_id).first()
        trades = db.query(Trades).filter(Trades.order_id == order.id).first()
        transfer = db.query(Transfers).filter(Transfers.order_id == order.id).first()
        money = transfer.quanitity * trades.price
        driver_balance = db.query(Users).filter(Users.id == transfer.driver_id).first()
        if order and order.status == 2 and driver_balance == money:
            new_income = Incomes(
                money=money,
                date=datetime.today(),
                comment=form.comment,
                kassa_id=form.kassa_id,
                user_id=thisuser.id,
                branch_id=thisuser.branch_id,
                source=form.source,
                source_id=form.source_id,
            )
            save_in_db(db, new_income)
            update_kassa_r(form.kassa_id, form.money, db, thisuser.id)
        else:
            raise HTTPException(status_code=400, detail="To'lov to'liq bo'maguncha, kirim qilib bo'lmaydi")

        old_kassa_balance = db.query(Kassas).filter(Kassas.id == form.kassa_id).first()
        new_balance = old_kassa_balance.balance + Decimal(form.money)
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: new_balance
        })
        db.commit()
                    # update_kassa_r(form.kassa_id,form.money,db,thisuser.id)

    elif form.source == "user" and kassa != None:
        user = db.query(Users).filter(Users.id == thisuser.id).first()
        if user.balance >= form.money:
            new_income = Incomes(
                money=form.money,
                date=datetime.today(),
                comment=form.comment,
                kassa_id=form.kassa_id,
                user_id=thisuser.id,
                branch_id=thisuser.branch_id,
                source=form.source,
                source_id=form.source_id,
            )
            save_in_db(db, new_income)
            update_kassa_r(form.kassa_id, form.money, db, thisuser.id)
            old_user_balance = db.query(Users).filter(Users.id == thisuser.id).first()
            new_balance = old_user_balance.balance - Decimal(form.money)
            db.query(Users).filter(Users.id == thisuser.id).update({
                Users.balance: new_balance
            })
            db.commit()
        else:
            raise HTTPException(status_code=400,detail="Balansizgizda yetarli mablag' yo'q yoki notogri malumot kiritdingiz")


def update_income_e(form, db, thisuser):
    allowed_time = timedelta(minutes=5)
    if the_one(form.id, Incomes, db).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    if the_one(form.source_id, Orders, db) and form.source == "order":
        old_money = get_in_db(db, Incomes, form.id).money
        db.query(Incomes).filter(Incomes.id == form.id).update({
            Incomes.money: form.money,
            Incomes.source: form.source,
            Incomes.source_id: form.source_id,
            Incomes.kassa_id: form.kassa_id,
            Incomes.comment: form.comment,
            Incomes.branch_id: thisuser.branch_id,
            Incomes.date: datetime.today(),
        })
        db.commit()
        new_money = get_in_db(db, Incomes, form.id).money
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - old_money + new_money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")


def delete_income_e(id, db):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Incomes, id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Incomes, id)
    db.query(Incomes).filter(Incomes.id == id).delete()
    db.commit()