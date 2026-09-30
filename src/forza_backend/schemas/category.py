from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=64)
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(None, min_length=1, max_length=64)
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: UUID
    category_name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)



