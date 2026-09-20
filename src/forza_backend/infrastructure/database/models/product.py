import sqlalchemy, uuid, decimal
from typing import Optional
from ..connection import Base
from ....core.enums.unit_of_measurements import UnitMeasurements
from ....core.exceptions import ProductNotFoundException
from sqlalchemy import ForeignKey, String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

class Product(Base):
    __tablename__ = "products"
    
    product_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    category_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        ForeignKey("categories.category_id"),
        nullable=False
    )
    
    sku: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )
    
    barcode: Mapped[Optional[str]] = mapped_column(
        String(14),
        nullable=True,
        unique=True
    )
    
    product_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    
    description: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    
    unit_measurement: Mapped[UnitMeasurements] = mapped_column(
        sqlalchemy.Enum(UnitMeasurements),
        nullable=False
    )
    
    cost_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    
    selling_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    
    reorder_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    
    category = relationship("Category", back_populates="products")
    
    @classmethod
    def get_by_id(cls, db: Session, product_id: uuid.UUID) -> "Product":
        product = db.query(cls).filter(cls.product_id == product_id).one_or_none()
        if not product:
            raise ProductNotFoundException("Product not found")
        return product