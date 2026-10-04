from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from .models.sale_item import SaleItem
from ...core.exceptions import DatabaseException

class SaleItemDatabase:
    @staticmethod
    def create_sale_item(db: Session, sale_item: SaleItem) -> SaleItem:
        db.add(sale_item)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException(
                "Failed to create sale item."
            ) from e

        return sale_item
    
    @staticmethod
    def list_by_sale_id(db: Session,sale_id: UUID) -> list[SaleItem]:
        return (
            db.query(SaleItem)
            .filter(SaleItem.sale_id == sale_id)
            .all()
        )