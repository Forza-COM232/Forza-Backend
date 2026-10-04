import sqlalchemy, uuid, decimal
from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from ..connection import Base
from ....core.exceptions import SaleNotFoundException
from ....core.enums.payment_method import PaymentMethodEnum

class Sale(Base):
    __tablename__ = "sales"

    sale_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    sold_by: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False
    )

    sale_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now()
    )

    total_amount: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=decimal.Decimal("0.00")
    )

    payment_method: Mapped[PaymentMethodEnum] = mapped_column(
        sqlalchemy.Enum(PaymentMethodEnum),
        nullable=False,
        default=PaymentMethodEnum.CASH
    )

    user = relationship("User")
    items = relationship( "SaleItem", back_populates="sale", cascade="all, delete-orphan")
    sale = relationship("Sale", back_populates="items")

    @classmethod
    def get_by_id(cls, db: Session, sale_id: uuid.UUID) -> "Sale":
        sale = db.query(cls).filter(cls.sale_id == sale_id).one_or_none()
        if not sale:
            raise SaleNotFoundException("Sale not found")
        return sale
