import sqlalchemy, uuid, decimal
from sqlalchemy import ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from ..connection import Base
from ....core.exceptions import PurchaseOrderItemNotFoundException

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    purchase_order_item_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    purchase_order_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("purchase_orders.purchase_order_id", ondelete="CASCADE"),
        nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_cost: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    total_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")

    @classmethod
    def get_by_id(cls, db: Session, purchase_order_item_id: uuid.UUID) -> "PurchaseOrderItem":
        item = db.query(cls).filter(cls.purchase_order_item_id == purchase_order_item_id).one_or_none()
        if not item:
            raise PurchaseOrderItemNotFoundException("Purchase order item not found")
        return item
