from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from .models.sale import Sale
from ...core.exceptions import DatabaseException

class SaleDatabase:
    @staticmethod
    def create_sale(db: Session, sale: Sale) -> Sale:
        db.add(sale)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to create sale.") from e

        return sale

    @staticmethod
    def get_sale_by_id(db: Session,sale_id: UUID) -> Sale:
        return Sale.get_by_id(db, sale_id)

    @staticmethod
    def list_sales(db: Session, skip: int = 0, limit: int = 50) -> list[Sale]:

        return (
            db.query(Sale)
            .order_by(Sale.sale_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )