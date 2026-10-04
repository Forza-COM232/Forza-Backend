import sqlalchemy, uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
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

    contact_name: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    phone: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    address: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

    @classmethod
    def get_by_id(cls, db: Session, supplier_id: uuid.UUID) -> "Supplier":
        supplier = db.query(cls).filter(cls.supplier_id == supplier_id).one_or_none()
        if not supplier:
            raise SupplierNotFoundException("Supplier not found")
        return supplier
