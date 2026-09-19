from pydantic import BaseModel, EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4

class Users(BaseModel):
    __tablename__ = "users"
    
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    email: Mapped[EmailStr] = mapped_column(
        String,
        nullable=False
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )