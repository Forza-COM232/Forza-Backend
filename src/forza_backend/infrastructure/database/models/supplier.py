import sqlalchemy, uuid
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from ..connection import Base
from ....core.exceptions import SupplierNotFoundException

class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    supplier_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    contact_name: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    email: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    address: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    @classmethod
    def get_by_id(cls, db: Session, supplier_id: uuid.UUID) -> "Supplier":
        supplier = db.query(cls).filter(cls.supplier_id == supplier_id).one_or_none()
        if not supplier:
            raise SupplierNotFoundException("Supplier not found")
        return supplier
