import sqlalchemy, uuid
from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from ..connection import Base
from ....core.exceptions import UserNotFoundException

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    stock_movement = relationship("StockMovement", back_populates="user")

    @classmethod
    def get_by_id(cls, db: Session, user_id: uuid.UUID) -> "User":
        user = db.query(cls).filter(cls.user_id == user_id).one_or_none()
        if not user:
            raise UserNotFoundException("User not found")
        return user

    @classmethod
    def get_by_email(cls, db: Session, email: EmailStr) -> "User":
        user_email = db.query(cls).filter(cls.email == email).one_or_none()
        if not user_email:
            raise UserNotFoundException("No user found with that email")
        return user_email