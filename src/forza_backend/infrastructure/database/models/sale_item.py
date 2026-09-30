import sqlalchemy, uuid, decimal
from sqlalchemy import ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from ..connection import Base
from ....core.exceptions import SaleItemNotFoundException

class SaleItem(Base):
    __tablename__ = "sale_items"

    sale_item_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    sale_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("sales.sale_id", ondelete="CASCADE"),
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

    unit_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    total_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    product = relationship("Product")

    @classmethod
    def get_by_id(cls, db: Session, sale_item_id: uuid.UUID) -> "SaleItem":
        sale_item = db.query(cls).filter(cls.sale_item_id == sale_item_id).one_or_none()
        if not sale_item:
            raise SaleItemNotFoundException("Sale item not found")
        return sale_item
