import os

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.paginatsiya import pagination
from models.products import Products


def all_products(search, page, limit, db, category_id, branch_id):
    products = db.query(Products).options(joinedload(Products.category))
    if branch_id > 0:
        products = products.filter(Products.branch_id == branch_id)
    if category_id > 0:
        products = products.filter(Products.category_id==category_id)
    if search:
        search_formatted = "%{}%".format(search)
        products = products.filter(Products.name.like(search_formatted))
    products = products.order_by(Products.id.desc())
    return pagination(products, page, limit)

# bitta productni malumotini olish uchun function
def one_product(db, ident):
    the_p = db.query(Products).filter(Products.id == ident).options(joinedload(Products.category)).first()
    if the_p is None:
        raise HTTPException(status_code=404)
    return the_p


def create_products_y(name, comment, price, litr, file, category_id, db, this_user):
    the_one(category_id, Categories, db)
    if file:
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpeg", ".png", ".jpg", ".svg"]:
            raise HTTPException(status_code=400, detail="The file format cannot macht!")
        with open(f"Uploaded/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        new_products_db = Products(
            name=name,
            comment=comment,
            price=price,
            litr=litr,
            file=file.filename,
            category_id=category_id,
            user_id=this_user.id,
            branch_id=this_user.branch_id
        )
        save_in_db(db, new_products_db)
    else:
        new_products_db = Products(
            name=name,
            comment=comment,
            price=price,
            litr=litr,
            file="",
            category_id=category_id,
            user_id=this_user.id,
            branch_id=this_user.branch_id
        )
        save_in_db(db, new_products_db)


def update_products_y(id, name, comment, price, litr, file, category_id, db, this_user):
    the_one(category_id, Categories, db)
    product = the_one(id, Products, db)
    if file:
        # Save the new file and update the "file" attribute
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpeg", ".png", ".jpg", ".svg"]:
            raise HTTPException(status_code=400, detail="The file format does not match!")
        os.unlink(f"upload_files/{product.file}")
        with open(f"upload_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        file_name = file.filename
    else:
        # Keep the existing file name
        file_name = product.file
        product.name = name
        product.comment = comment
        product.price = price
        product.litr = litr
        product.file = file_name
        product.category_id = category_id
        product.user_id = this_user.id
        product.branch_id=this_user.branch_id

        db.commit()



