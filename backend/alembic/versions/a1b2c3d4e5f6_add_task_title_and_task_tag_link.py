"""add task title and task_tag link table

Revision ID: a1b2c3d4e5f6
Revises: dac6eb355023
Create Date: 2026-07-24 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'dac6eb355023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Необязательный заголовок задачи.
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))

    # Связь многие-ко-многим между задачами и тегами.
    op.create_table(
        'tasktaglink',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['task.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id']),
        sa.PrimaryKeyConstraint('task_id', 'tag_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('tasktaglink')

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('title')
