from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from ..core.enums.payment_method import PaymentMethodEnum


class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)

class SaleCreate(BaseModel):
    payment_method: PaymentMethodEnum
    items: list[SaleItemCreate] = Field(min_length=1)
