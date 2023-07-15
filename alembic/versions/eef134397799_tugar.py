"""tugar

Revision ID: eef134397799
Revises: 0836d8d3d9a6
Create Date: 2023-07-11 17:58:23.384841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eef134397799'
down_revision = '0836d8d3d9a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('warehouses_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=999), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('warehouses', sa.Column('address', sa.String(length=999), nullable=True))
    op.add_column('warehouses', sa.Column('map_long', sa.String(length=999), nullable=True))
    op.add_column('warehouses', sa.Column('map_lat', sa.String(length=999), nullable=True))
    op.drop_column('warehouses', 'product_id')
    op.drop_column('warehouses', 'price')
    op.drop_column('warehouses', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('warehouses', sa.Column('quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('warehouses', sa.Column('price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('warehouses', sa.Column('product_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('warehouses', 'map_lat')
    op.drop_column('warehouses', 'map_long')
    op.drop_column('warehouses', 'address')
    op.drop_table('warehouses_products')
    # ### end Alembic commands ###