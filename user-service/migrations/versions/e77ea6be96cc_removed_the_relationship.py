"""Removed the relationship

Revision ID: e77ea6be96cc
Revises: 7b19fd27fd71
Create Date: 2024-11-18 21:40:07.533383

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e77ea6be96cc"
down_revision: Union[str, None] = "7b19fd27fd71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
