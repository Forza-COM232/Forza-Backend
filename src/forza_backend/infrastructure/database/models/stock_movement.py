import sqlalchemy, uuid
from ..connection import Base
from ....core.enums.movement_types import MovementType
from ....core.exceptions import StockMovementNotFoundException
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    stock_movement_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    product_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False
    )
    
    performed_by: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False
    )
    
    movement_type: Mapped[MovementType] = mapped_column(
        sqlalchemy.Enum(MovementType),
        nullable=False
    )
    
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    reason: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    
    user = relationship("User", back_populates="stock_movement")
    product = relationship("Product", back_populates="stock_movement")

    @classmethod
    def get_by_id(cls, db: Session, stock_movement_id: uuid.UUID) -> "StockMovement":
        stock_movement = db.query(cls).filter(cls.stock_movement_id == stock_movement_id).one_or_none()
        if not stock_movement:
            raise StockMovementNotFoundException("Stock Movement not found")
        return stock_movement