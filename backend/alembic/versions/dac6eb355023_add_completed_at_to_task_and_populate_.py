"""add completed_at to task and populate from created_at

Revision ID: dac6eb355023
Revises: 
Create Date: 2026-05-11 14:06:43.216774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dac6eb355023'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # Шаг 1: Добавляем колонку, временно разрешая пустоты (nullable=True)
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_at', sa.DateTime(), nullable=True))

    # Шаг 2: Копируем данные из created_at в completed_at
    # (Выполняется вне блока batch_op, чтобы колонка уже физически существовала в базе)
    op.execute("UPDATE task SET completed_at = created_at WHERE status = 1")

    # Шаг 3: Делаем колонку обязательной (запрещаем NULL)
    # with op.batch_alter_table('task', schema=None) as batch_op:
    #     batch_op.alter_column('completed_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    
    # При откате миграции просто удаляем колонку
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('completed_at')