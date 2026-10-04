from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models.stock_movement import StockMovement
from ...core.exceptions import DatabaseException


class StockMovementDatabase:
    @staticmethod
    def create_stock_movement(db: Session, stock_movement: StockMovement) -> StockMovement:
        db.add(stock_movement)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException(
                "Failed to create stock movement."
            ) from e
        return stock_movement

    @staticmethod
    def get_stock_movement_by_id(db: Session, stock_movement_id: UUID) -> StockMovement:
        return StockMovement.get_by_id(db, stock_movement_id)

    @staticmethod
    def list_stock_movements(db: Session, skip: int = 0, limit: int = 50) -> list[StockMovement]:
        return (
            db.query(StockMovement)
            .order_by(
                StockMovement.stock_movement_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def list_by_product_id(db: Session, product_id: UUID, skip: int = 0, limit: int = 50) -> list[StockMovement]:
        return (
            db.query(StockMovement)
            .filter(
                StockMovement.product_id == product_id
            )
            .order_by(
                StockMovement.stock_movement_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )