from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from functions.products_func import all_products, create_products_y, update_products_y, one_product
from models.products import Products
from utils.auth import get_current_user
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from schemas.products_schemas import CreateProducts,UpdateProducts
from db import database
from utils.role_checker import *

products_router = APIRouter(
    prefix="/products",
    tags=["Products operation"]
)


@products_router.get("/get_products")
def get_products(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_user),category_id: int = 0,branch_id: int = 0):
    role_verification(user=current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return one_product(db, id)
    return all_products(search, page, limit, db,category_id,branch_id)


@products_router.post("/create_products")
def create_products(name: str, comment: str, price: float, litr: float,
                    file: UploadFile = File(None), category_id: int = Form(0), db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    
    role_verification(user=current_user)
    create_products_y(name, comment, price, litr, file, category_id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@products_router.put("/update_products")
def update_products(id: int = Form(0), name: str = Form(None), comment: str = Form(None),
                    price: float = Form(0), litr: float = Form(1),
                    file: UploadFile = File(None), category_id: int = Form(0), db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_verification(user=current_user)
    update_products_y(id, name, comment, price, litr, file, category_id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






