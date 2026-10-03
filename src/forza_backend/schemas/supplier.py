from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SupplierCreate(BaseModel):
    supplier_name: str = Field(..., min_length=1, max_length=255)
    contact_name: str = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: str = Field(None, max_length=50)
    address: str = None

class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None

class SupplierResponse(BaseModel):
    supplier_id: UUID
    supplier_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
