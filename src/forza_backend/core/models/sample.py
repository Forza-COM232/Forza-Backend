# Any data models will be put on this folder.
# Don't put anything on this file, create your own file and make sure to have meaningful name.

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import uuid4, UUID

class Base(DeclarativeBase):
    ...

class SampleModel(Base):
    __tablename__ = "sample"
    
    sample_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )