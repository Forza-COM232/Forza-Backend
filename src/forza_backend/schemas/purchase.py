from pydantic import BaseModel, Field
from decimal import Decimal
from uuid import UUID
from typing import Optional
from ..core.enums.purchase_order_status import PurchaseOrderStatusEnum

class PurchaseOrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    unit_cost: Decimal = Field(gt=0)

class PurchaseOrderCreate(BaseModel):
    supplier_id: UUID
    purchase_order_item: list[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(BaseModel):
    status: Optional[PurchaseOrderStatusEnum] = None