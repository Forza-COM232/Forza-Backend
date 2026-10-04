from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from .models.purchase_order import PurchaseOrder
from ...core.exceptions import DatabaseException

class PurchaseOrderDatabase:
    @staticmethod
    def create_purchase_order(db: Session, purchase_order: PurchaseOrder) -> PurchaseOrder:
        db.add(purchase_order)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to create purchase order.") from e
        db.refresh(purchase_order)
        return purchase_order
    
    @staticmethod
    def get_purchase_order(db: Session, purchase_order_id: UUID) -> PurchaseOrder:
        return PurchaseOrder.get_by_id(db, purchase_order_id)
    
    @staticmethod
    def list_purchase_orders(db: Session, skip: int = 0, limit: int = 0) -> list[PurchaseOrder]:
        return (
            db.query(PurchaseOrder)
            .order_by(PurchaseOrder.purchase_order_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def update_purchase_order(db: Session, purchase_order: PurchaseOrder) -> PurchaseOrder:
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to update purchase order.") from e
        return purchase_order
    
    @staticmethod
    def delete_purchase_order(db: Session, purchase_order_id: UUID) -> None:
        po = PurchaseOrder.get_by_id(db, purchase_order_id)
        try:
            db.delete(po)
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to delete purchase order.") from e