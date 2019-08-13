"""empty message

Revision ID: ad9b76e27fe9
Revises: 
Create Date: 2019-08-14 01:22:38.611732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad9b76e27fe9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('application_status')
    op.add_column('application_details', sa.Column('status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application_details', 'status')
    op.create_table('application_status',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('application_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('remarks', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('reviewed_on', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], [u'application_details.id'], name=u'application_status_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    # ### end Alembic commands ###
