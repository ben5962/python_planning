"""ajout d une clef primaire Ó la table principale

Revision ID: 268d3e84751f
Revises: 
Create Date: 2017-07-19 22:47:04.906631

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import (create_engine, Column, Integer, Numeric, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# revision identifiers, used by Alembic.
revision = '268d3e84751f'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    #batch_op = op.batch_alter_table("planning")
    with op.batch_alter_table("planning") as batch_op:
        if ('Column' in dir()):
            batch_op.add_column(Column('idx_planning', Integer,primary_key=True, autoincrement="auto"))
        else:
            raise ImportError("vérifier espace de nom: Column pas visible depuis ".___file___)
        #batch_op.batch_create_primary_key("planning_idx", "planning", ['debut_poste', 'fin_poste'])
        


def downgrade():
    with op.batch_alter_table("planning") as batch_op:
        batch_op.batch_drop_column('planning_idx')
