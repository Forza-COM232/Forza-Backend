from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..core.exceptions import DatabaseException, DuplicateException, InvalidBarcodeException
from ..infrastructure.database.models.category import Category
from ..infrastructure.database.models.product import Product
from ..schemas.product import ProductUpdate


class ProductService:
    @staticmethod
    def get_product(db: Session, product_id: UUID) -> Product:
        return Product.get_by_id(db, product_id)

    @staticmethod
    def list_products(
        db: Session,
        category_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Product]:
        query = db.query(Product)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.order_by(Product.product_name).offset(skip).limit(limit).all()

    @staticmethod
    def update_product(db: Session, product_id: UUID, data: ProductUpdate) -> Product:
        product = Product.get_by_id(db, product_id)

        changes = data.model_dump(exclude_unset=True)
        if "category_id" in changes and changes["category_id"] is not None:
            Category.get_by_id(db, changes["category_id"])

        for field, value in changes.items():
            setattr(product, field, value)

        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise DuplicateException("This product already exists") from exc
        db.refresh(product)
        return product
    
    @staticmethod
    def validate_barcode(barcode: Optional[str]) -> None:
        if barcode is not None and len(barcode) > 14:
            raise InvalidBarcodeException("Barcode must be at most 14 characters long")