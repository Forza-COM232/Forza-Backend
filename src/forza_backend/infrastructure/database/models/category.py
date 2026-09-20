import sqlalchemy, uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from ..connection import Base
from ....core.exceptions import CategoryNotFoundException

class Category(Base):
    __tablename__ = "categories"
    
    category_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    category_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    description: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    
    product = relationship("Product", back_populates="category")
    
    @classmethod
    def get_by_id(cls, db: Session, category_id: uuid.UUID) -> "Category":
        category = db.query(cls).filter(cls.category_id == category_id).one_or_none()
        if not category:
            raise CategoryNotFoundException("Category not found")
        return category