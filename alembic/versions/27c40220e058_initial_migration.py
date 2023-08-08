"""Initial migration

Revision ID: 27c40220e058
Revises: 6acf307ab804
Create Date: 2023-08-05 08:13:06.576995

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '27c40220e058'
down_revision = '6acf307ab804'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contracts', sa.Column('name', sa.String(length=999), nullable=True))
    op.drop_column('contracts', 'warehouse_product_id')
    op.add_column('customer_loc_products', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('expenses', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('expenses', sa.Column('type', sa.String(length=999), nullable=True))
    op.add_column('incomes', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('incomes', sa.Column('type', sa.String(length=999), nullable=True))
    op.add_column('orders', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('orders', sa.Column('orienter', sa.String(length=999), nullable=True))
    op.add_column('supplies', sa.Column('name', sa.String(length=999), nullable=True))
    op.drop_column('supplies', 'warehouse_product_id')
    op.add_column('trades', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('transfers', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('transfers', sa.Column('product_id', sa.Integer(), nullable=True))
    op.drop_column('transfers', 'warehouse_product_id')
    op.drop_column('transfers', 'order_id')
    op.add_column('user_products', sa.Column('name', sa.String(length=999), nullable=True))
    op.add_column('user_products', sa.Column('product_id', sa.Integer(), nullable=True))
    op.drop_column('user_products', 'warehouse_product_id')
    op.add_column('warehouses_products', sa.Column('name', sa.String(length=999), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('warehouses_products', 'name')
    op.add_column('user_products', sa.Column('warehouse_product_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('user_products', 'product_id')
    op.drop_column('user_products', 'name')
    op.add_column('transfers', sa.Column('order_id', mysql.INTEGER(display_width=20), autoincrement=False, nullable=True))
    op.add_column('transfers', sa.Column('warehouse_product_id', mysql.INTEGER(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('transfers', 'product_id')
    op.drop_column('transfers', 'name')
    op.drop_column('trades', 'name')
    op.add_column('supplies', sa.Column('warehouse_product_id', mysql.INTEGER(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('supplies', 'name')
    op.drop_column('orders', 'orienter')
    op.drop_column('orders', 'name')
    op.drop_column('incomes', 'type')
    op.drop_column('incomes', 'name')
    op.drop_column('expenses', 'type')
    op.drop_column('expenses', 'name')
    op.drop_column('customer_loc_products', 'name')
    op.add_column('contracts', sa.Column('warehouse_product_id', mysql.INTEGER(display_width=20), autoincrement=False, nullable=True))
    op.drop_column('contracts', 'name')
    # ### end Alembic commands ###