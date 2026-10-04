from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from .models.inventory import Inventory
from ...core.exceptions import DatabaseException

class InventoryDatabase():
    @staticmethod
    def create_inventory(db: Session, inventory: Inventory) -> Inventory:
        db.add(inventory)
        try:
            db.flush()
        except IntegrityError as e:
            raise DatabaseException("Failed to create inventory") from e
        db.refresh(inventory)
        return inventory
    
    @staticmethod
    def get_inventory_by_id(db: Session, inventory_id: UUID) -> Inventory:
        return Inventory.get_by_id(db, inventory_id)
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: UUID) -> Inventory:
        return Inventory.get_by_product_id(db, product_id)
    
    @staticmethod
    def list_inventories(db: Session, skip: int = 0, limit: int = 50) -> list[Inventory]:
        return (
            db.query(Inventory)
            .order_by(Inventory.inventory_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    @staticmethod
    def update_inventory(db: Session, inventory: Inventory) -> Inventory:
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException(
                "Failed to update inventory."
            ) from e

        return inventory