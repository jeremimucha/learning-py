"""Add readers_books

Revision ID: 2322a8064857
Revises: a9587d5f11d4
Create Date: 2022-10-01 19:25:51.396239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2322a8064857'
down_revision = 'a9587d5f11d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('readers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('readers_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('reader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['readers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_readers_books_book_id'), 'readers_books', ['book_id'], unique=False)
    op.create_index(op.f('ix_readers_books_reader_id'), 'readers_books', ['reader_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_readers_books_reader_id'), table_name='readers_books')
    op.drop_index(op.f('ix_readers_books_book_id'), table_name='readers_books')
    op.drop_table('readers_books')
    op.drop_table('readers')
    op.drop_table('books')
    # ### end Alembic commands ###
