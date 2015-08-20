"""empty message

Revision ID: 11939eba9b7
Revises: 4f87da8586
Create Date: 2015-08-20 13:48:37.518136

"""

# revision identifiers, used by Alembic.
revision = '11939eba9b7'
down_revision = '4f87da8586'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_documents_name_url', table_name='documents')
    op.create_index('idx_documents_name_url', 'documents', ['name', 'url'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_documents_name_url', table_name='documents')
    op.create_index('idx_documents_name_url', 'documents', ['name', 'url'], unique=False)
    ### end Alembic commands ###
