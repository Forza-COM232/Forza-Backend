import sqlalchemy, uuid, decimal
from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from ..connection import Base
from ....core.exceptions import PurchaseOrderNotFoundException
from ....core.enums.purchase_order_status import PurchaseOrderStatusEnum

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    purchase_order_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("suppliers.supplier_id", ondelete="RESTRICT"),
        nullable=False
    )

    ordered_by: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False
    )
    
    # received_by: Mapped[uuid.UUID] = mapped_column(
    #     sqlalchemy.UUID(as_uuid=True),
    #     ForeignKey("users.user_id", ondelete="RESTRICT"),
    #     nullable=False
    # )

    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now()
    )

    status: Mapped[PurchaseOrderStatusEnum] = mapped_column(
        sqlalchemy.Enum(PurchaseOrderStatusEnum),
        nullable=False,
        default=PurchaseOrderStatusEnum.PENDING
    )

    total_amount: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=decimal.Decimal("0.00")
    )

    supplier = relationship("Supplier", back_populates="purchase_orders")
    user = relationship("User", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")

    @classmethod
    def get_by_id(cls, db: Session, purchase_order_id: uuid.UUID) -> "PurchaseOrder":
        purchase_order = db.query(cls).filter(cls.purchase_order_id == purchase_order_id).one_or_none()
        if not purchase_order:
            raise PurchaseOrderNotFoundException("Purchase order not found")
        return purchase_order
