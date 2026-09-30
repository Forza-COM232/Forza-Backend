from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..core.enums.movement_types import MovementType

class StockMovementCreate(BaseModel):
    product_id: UUID
    movement_type: MovementType
    performed_by: UUID
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None

class StockMovementResponse(BaseModel):
    stock_movement_id: UUID

    model_config = ConfigDict(from_attributes=True)
