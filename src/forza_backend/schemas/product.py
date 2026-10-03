from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..core.enums.unit_of_measurements import UnitMeasurements


class ProductCreate(BaseModel):
    category_id: UUID
    sku: str = Field(..., min_length=1, max_length=64)
    barcode: Optional[str] = Field(None, min_length=1, max_length=14)
    product_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    unit_measurement: UnitMeasurements
    cost_price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    selling_price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    reorder_level: int = Field(0, ge=0)

class ProductUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=64)
    barcode: Optional[str] = Field(None, min_length=1, max_length=14)
    product_name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    unit_measurement: Optional[UnitMeasurements] = None
    cost_price: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    selling_price: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    reorder_level: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
    product_id: UUID

    model_config = ConfigDict(from_attributes=True)