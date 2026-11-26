"""Rutas de salida del resultado: volumen 3D usado y PNG de la ROI

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-26
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Nulas: un resultado anterior a esta migración solo tiene la máscara
    with op.batch_alter_table("resultado") as tabla:
        tabla.add_column(sa.Column("ruta_imagen", sa.String(255)))
        tabla.add_column(sa.Column("ruta_roi", sa.String(255)))


def downgrade() -> None:
    with op.batch_alter_table("resultado") as tabla:
        tabla.drop_column("ruta_roi")
        tabla.drop_column("ruta_imagen")
