from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InventoryResponse(BaseModel):
    inventory_id: UUID
    product_id: UUID
    quantity_on_hand: int

    model_config = ConfigDict(from_attributes=True)