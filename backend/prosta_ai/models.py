"""Tablas de la base de datos (arquitectura de datos 1.3.2.5, alcance del ciclo 6)."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR, BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Identity, Index,
    Integer, Numeric, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from prosta_ai.db import Base, ahora
from prosta_ai.pipeline.stages import STAGES

FORMATOS = ("DICOM", "NIfTI")
ESTADOS_ADMISION = ("admitido", "no compatible")
ESTADOS = ("pendiente", "en proceso", "completado", "fallido")


def _en_lista(columna: str, valores) -> str:
    return f"{columna} IN (" + ", ".join(f"'{v}'" for v in valores) + ")"


def _fecha(**kw):
    return mapped_column(DateTime(timezone=True), **kw)


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    alias: Mapped[str] = mapped_column(String(30), unique=True)
    hash_contrasena: Mapped[str] = mapped_column(String(255))
    fecha_creacion: Mapped[datetime] = _fecha(default=ahora)

    estudios: Mapped[list["Estudio"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True
    )


class Estudio(Base):
    __tablename__ = "estudio"
    __table_args__ = (
        CheckConstraint(_en_lista("formato", FORMATOS), name="ck_estudio_formato"),
        CheckConstraint(
            _en_lista("estado_admision", ESTADOS_ADMISION), name="ck_estudio_estado_admision"
        ),
        Index("ix_estudio_id_usuario", "id_usuario"),
    )

    id_estudio: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    codigo_anonimo: Mapped[str] = mapped_column(String(12), unique=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    formato: Mapped[str] = mapped_column(String(5))
    fecha_carga: Mapped[datetime] = _fecha(default=ahora)
    estado_admision: Mapped[str] = mapped_column(String(15))

    usuario: Mapped[Usuario] = relationship(back_populates="estudios")
    archivos: Mapped[list["Archivo"]] = relationship(
        back_populates="estudio", cascade="all, delete-orphan", passive_deletes=True
    )
    trabajos: Mapped[list["Trabajo"]] = relationship(
        back_populates="estudio", cascade="all, delete-orphan", passive_deletes=True,
        order_by="Trabajo.id_trabajo",
    )


class Archivo(Base):
    """Archivo guardado en disco; la base solo conserva ruta y huella (RB-02)."""

    __tablename__ = "archivo"

    id_archivo: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    id_estudio: Mapped[int] = mapped_column(ForeignKey("estudio.id_estudio", ondelete="CASCADE"))
    ruta: Mapped[str] = mapped_column(String(255))
    tamano_bytes: Mapped[int] = mapped_column(BigInteger)
    hash_sha256: Mapped[str] = mapped_column(CHAR(64))
    valido: Mapped[bool] = mapped_column(Boolean, default=True)

    estudio: Mapped[Estudio] = relationship(back_populates="archivos")


class Modelo(Base):
    __tablename__ = "modelo"
    __table_args__ = (UniqueConstraint("nombre", "version", name="uq_modelo_nombre_version"),)

    id_modelo: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    version: Mapped[str] = mapped_column(String(20))
    ruta_pesos: Mapped[str | None] = mapped_column(String(255))
    hash_pesos: Mapped[str | None] = mapped_column(CHAR(64))
    ruta_configuracion: Mapped[str | None] = mapped_column(String(255))
    fecha_registro: Mapped[datetime] = _fecha(default=ahora)


class Trabajo(Base):
    """Procesamiento de un estudio en segundo plano (CU03)."""

    __tablename__ = "trabajo"
    __table_args__ = (
        CheckConstraint(_en_lista("estado", ESTADOS), name="ck_trabajo_estado"),
        Index("ix_trabajo_estado", "estado"),
    )

    id_trabajo: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    id_estudio: Mapped[int] = mapped_column(ForeignKey("estudio.id_estudio", ondelete="CASCADE"))
    id_modelo: Mapped[int] = mapped_column(ForeignKey("modelo.id_modelo"))
    estado: Mapped[str] = mapped_column(String(12), default="pendiente")
    fecha_creacion: Mapped[datetime] = _fecha(default=ahora)
    fecha_inicio: Mapped[datetime | None] = _fecha()
    fecha_fin: Mapped[datetime | None] = _fecha()
    etapa_fallida: Mapped[str | None] = mapped_column(String(25))
    mensaje_error: Mapped[str | None] = mapped_column(Text)

    estudio: Mapped[Estudio] = relationship(back_populates="trabajos")
    modelo: Mapped[Modelo] = relationship()
    etapas: Mapped[list["EtapaTrabajo"]] = relationship(
        back_populates="trabajo", cascade="all, delete-orphan", passive_deletes=True,
        order_by="EtapaTrabajo.id_etapa",
    )
    resultado: Mapped["Resultado | None"] = relationship(
        back_populates="trabajo", cascade="all, delete-orphan", passive_deletes=True,
        uselist=False,
    )


class EtapaTrabajo(Base):
    __tablename__ = "etapa_trabajo"
    __table_args__ = (
        CheckConstraint(_en_lista("nombre", STAGES), name="ck_etapa_nombre"),
        CheckConstraint(_en_lista("estado", ESTADOS), name="ck_etapa_estado"),
    )

    id_etapa: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    id_trabajo: Mapped[int] = mapped_column(ForeignKey("trabajo.id_trabajo", ondelete="CASCADE"))
    nombre: Mapped[str] = mapped_column(String(25))
    estado: Mapped[str] = mapped_column(String(12), default="pendiente")
    fecha_inicio: Mapped[datetime | None] = _fecha()
    fecha_fin: Mapped[datetime | None] = _fecha()
    duracion_s: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    trabajo: Mapped[Trabajo] = relationship(back_populates="etapas")


class Resultado(Base):
    """Máscara y ROI de un trabajo; Dice e IoU solo si hay referencia (CU04)."""

    __tablename__ = "resultado"
    __table_args__ = (
        CheckConstraint("dice IS NULL OR (dice >= 0 AND dice <= 1)", name="ck_resultado_dice"),
        CheckConstraint("iou IS NULL OR (iou >= 0 AND iou <= 1)", name="ck_resultado_iou"),
    )

    id_resultado: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    id_trabajo: Mapped[int] = mapped_column(
        ForeignKey("trabajo.id_trabajo", ondelete="CASCADE"), unique=True
    )
    ruta_mascara: Mapped[str] = mapped_column(String(255))
    dice: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    iou: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    tiempo_total_s: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    fecha_registro: Mapped[datetime] = _fecha(default=ahora)

    trabajo: Mapped[Trabajo] = relationship(back_populates="resultado")
