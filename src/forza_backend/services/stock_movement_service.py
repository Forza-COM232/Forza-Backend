from uuid import UUID

from sqlalchemy.orm import Session

from ..infrastructure.database.models.stock_movement import StockMovement
from ..infrastructure.database.stock_movement_database import StockMovementDatabase
from ..infrastructure.database.product_database import ProductDatabase
from ..infrastructure.database.user_database import UserDatabase

from ..core.enums.movement_types import MovementType
from ..core.exceptions import UserAlreadyDeactivatedException, InvalidStockMovementException


class StockMovementService:
    @staticmethod
    def get_stock_movement_by_id(db: Session, stock_movement_id: UUID) -> StockMovement:
        return StockMovementDatabase.get_stock_movement_by_id(db, stock_movement_id)

    @staticmethod
    def list_stock_movements(db: Session, skip: int = 0, limit: int = 50) -> list[StockMovement]:
        return StockMovementDatabase.list_stock_movements(db, skip, limit)

    @staticmethod
    def list_product_movements(db: Session, product_id: UUID, skip: int = 0, limit: int = 50) -> list[StockMovement]:
        return StockMovementDatabase.list_by_product_id(db, product_id, skip, limit)
    
    @staticmethod
    def create_stock_in(db: Session, product_id: UUID, performed_by: UUID, quantity: int, reason: str | None = None) -> StockMovement:
        if quantity <= 0:
            raise InvalidStockMovementException("Stock-in quantity must be greater than zero.")

        return StockMovementService._create_movement(
            db=db,
            product_id=product_id,
            performed_by=performed_by,
            movement_type=MovementType.STOCK_IN,
            quantity_delta=quantity,
            reason=reason
        )

    @staticmethod
    def create_stock_out(db: Session, product_id: UUID, performed_by: UUID, quantity: int, reason: str | None = None) -> StockMovement:
        if quantity <= 0:
            raise InvalidStockMovementException("Stock-out quantity must be greater than zero.")

        return StockMovementService._create_movement(
            db=db,
            product_id=product_id,
            performed_by=performed_by,
            movement_type=MovementType.STOCK_OUT,
            quantity_delta=-quantity,
            reason=reason
        )
    
    @staticmethod
    def create_adjustment(db: Session, product_id: UUID, performed_by: UUID, quantity_delta: int, reason: str) -> StockMovement:
        if quantity_delta == 0:
            raise InvalidStockMovementException("Adjustment cannot be zero.")

        return StockMovementService._create_movement(
            db=db,
            product_id=product_id,
            performed_by=performed_by,
            movement_type=MovementType.ADJUSTMENT,
            quantity_delta=quantity_delta,
            reason=reason
        )

    @staticmethod
    def _create_movement(db: Session, product_id: UUID, performed_by: UUID, movement_type: MovementType, quantity_delta: int, reason: str | None = None) -> StockMovement:
        product = ProductDatabase.get_product(db, product_id)
        user = UserDatabase.get_user_by_id(db, performed_by)

        if not user.is_active:
            raise UserAlreadyDeactivatedException("Inactive user cannot perform stock movement.")

        if quantity_delta == 0:
            raise InvalidStockMovementException("Stock movement quantity cannot be zero.")

        movement = StockMovement(
            product_id=product.product_id,
            performed_by=user.user_id,
            movement_type=movement_type,
            quantity_delta=quantity_delta,
            reason=reason
        )

        return StockMovementDatabase.create_stock_movement(db, movement)