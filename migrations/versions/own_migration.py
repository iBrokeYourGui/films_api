"""добавляем данные в поле test

Revision ID: f1262b9efe78
Revises: f1262b9efe77
Create Date: 2021-02-19 09:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# обязательно следим за последовательностью ревизий
from sqlalchemy import text

revision = 'f1262b9efe78'
down_revision = 'f1262b9efe77'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                UPDATE films
                SET test = 100
                WHERE title like '%Deathly%'
            """
        )
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                UPDATE films
                SET test = NULL
                WHERE title like '%Deathly'
            """
        )
    )
