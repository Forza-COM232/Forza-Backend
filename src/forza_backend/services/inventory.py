from uuid import UUID

from sqlalchemy.orm import Session

from ..infrastructure.database.models.inventory import Inventory
from ..infrastructure.database.models.product import Product


class InventoryService:

    @staticmethod
    def create_inventory(db: Session, product_id: UUID, quantity_on_hand: int = 0) -> Inventory:
        Product.get_by_id(db, product_id)
        inventory = Inventory(product_id=product_id, quantity_on_hand=quantity_on_hand)
        db.add(inventory)
        db.flush()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def get_inventory(db: Session, inventory_id: UUID) -> Inventory:
        return Inventory.get_by_id(db, inventory_id)

    @staticmethod
    def get_by_product(db: Session, product_id: UUID) -> Inventory:
        return Inventory.get_by_product_id(db, product_id)