import sqlalchemy, uuid
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from ..connection import Base
from ....core.exceptions import InventoryNotFoundException

class Inventory(Base):
    __tablename__ = "inventories"

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True
    )

    quantity_on_hand: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    location: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    product = relationship("Product", back_populates="inventory")

    @classmethod
    def get_by_id(cls, db: Session, inventory_id: uuid.UUID) -> "Inventory":
        inventory = db.query(cls).filter(cls.inventory_id == inventory_id).one_or_none()
        if not inventory:
            raise InventoryNotFoundException("Inventory not found")
        return inventory

    @classmethod
    def get_by_product_id(cls, db: Session, product_id: uuid.UUID) -> "Inventory":
        inventory = db.query(cls).filter(cls.product_id == product_id).one_or_none()
        if not inventory:
            raise InventoryNotFoundException("Inventory for product not found")
        return inventory
