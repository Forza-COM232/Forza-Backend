from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ...schemas.product import ProductCreate, ProductUpdate
from .models.product import Product
from ...core.exceptions import DuplicateException, DatabaseException, InvalidBarcodeException
from .models.category import Category


class ProductDatabase:
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        
        db.add(product)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DuplicateException("This product already exists") from e
        db.refresh(product)
        return product
    
    @staticmethod
    def get_product(db: Session, product_id: UUID) -> Product:
        return Product.get_by_id(db, product_id)
    
    @staticmethod
    def list_products(
        db: Session,
        category_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 50
    ) -> list[Product]:
        query = db.query(Product)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.order_by(Product.product_name).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: UUID, update_data: ProductUpdate) -> Product:
        product = Product.get_by_id(db, product_id)

        changes = update_data.model_dump(exclude_unset=True)
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
    def delete_product(db: Session, product_id: UUID) -> None:
        product = Product.get_by_id(db, product_id)
        db.delete(product)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            # This error occurs when trying to delete a product that has associated stock movements
            raise DatabaseException("Restricted action due to stock movement of the product") from exc