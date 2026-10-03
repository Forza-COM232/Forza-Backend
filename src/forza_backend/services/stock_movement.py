from uuid import UUID

from sqlalchemy.orm import Session

from ..infrastructure.database.models.product import Product
from ..infrastructure.database.models.stock_movement import StockMovement
from ..infrastructure.database.models.users import User
from ..schemas.stock_movement import StockMovementCreate


class StockMovementService:

    @staticmethod
    def create_stock_movement(db: Session, data: StockMovementCreate,) -> StockMovement:
        
        Product.get_by_id(db, data.product_id)
        User.get_by_id(db, data.performed_by)

        movement = StockMovement(**data.model_dump())
        db.add(movement)
        db.flush()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_stock_movement(db: Session, stock_movement_id: UUID,) -> StockMovement:
        return StockMovement.get_by_id(db, stock_movement_id)