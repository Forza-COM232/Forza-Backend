from uuid import UUID

from sqlalchemy.orm import Session

from ..infrastructure.database.models.inventory import Inventory
from ..infrastructure.database.inventory_database import InventoryDatabase
from ..services.stock_movement_service import StockMovementService
from ..core.exceptions import InvalidInventoryQuantityException, InsufficientStockException

class InventoryService:
    @staticmethod
    def get_inventory(db: Session, inventory_id: UUID) -> Inventory:
        return InventoryDatabase.get_inventory_by_id(db, inventory_id)

    @staticmethod
    def get_inventory_by_product(db: Session, product_id: UUID) -> Inventory:
        return InventoryDatabase.get_product_by_id(db, product_id)
    
    @staticmethod
    def list_inventory(db: Session, skip: int = 0, limit: int = 50) -> list[Inventory]:
        return InventoryDatabase.list_inventories(
            db,
            skip,
            limit
        )
    
    @staticmethod
    def increase_stock(db: Session, product_id: UUID, quantity: int) -> Inventory:
        if quantity <= 0:
            raise InvalidInventoryQuantityException("Quantity must be greater than zero.")

        inventory = InventoryDatabase.get_product_by_id(db, product_id)
        inventory.quantity_on_hand += quantity
        
        return InventoryDatabase.update_inventory(db, inventory)
    
    @staticmethod
    def decrease_stock(db: Session, product_id: UUID, quantity: int) -> Inventory:
        if quantity <= 0:
            raise InvalidInventoryQuantityException("Quantity must be greater than zero.")

        inventory = InventoryDatabase.get_product_by_id(db, product_id)
        if inventory.quantity_on_hand < quantity:
            raise InsufficientStockException("Insufficient stock.")
        inventory.quantity_on_hand -= quantity

        return InventoryDatabase.update_inventory(db, inventory)
    
    @staticmethod
    def adjust_stock(db: Session, product_id: UUID, new_quantity: int, performed_by: UUID, reason: str
    ) -> Inventory:
        if new_quantity < 0:
            raise InvalidInventoryQuantityException("Inventory quantity cannot be negative.")

        inventory = InventoryDatabase.get_product_by_id(db, product_id)

        current_quantity = inventory.quantity_on_hand
        quantity_delta = new_quantity - current_quantity

        if quantity_delta == 0:
            raise InvalidInventoryQuantityException("Inventory adjustment cannot result in the same quantity.")
        inventory.quantity_on_hand = new_quantity

        InventoryDatabase.update_inventory(db, inventory)

        StockMovementService.create_adjustment(
            db=db,
            product_id=product_id,
            performed_by=performed_by,
            quantity_delta=quantity_delta,
            reason=reason
        )

        return inventory
