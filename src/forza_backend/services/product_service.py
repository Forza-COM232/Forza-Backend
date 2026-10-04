from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..infrastructure.database.product_database import ProductDatabase
from ..infrastructure.database.models.category import Category
from ..core.sku import generate_sku
from ..core.exceptions import DuplicateException, InvalidBarcodeException, ProductNotFoundException
from ..infrastructure.database.models.category import Category
from ..infrastructure.database.models.product import Product
from ..schemas.product import ProductUpdate, ProductCreate


class ProductService:
    def __init__ (self) -> None:
        self.product_database = ProductDatabase()
    
    def create_product(self, db: Session, product_data: ProductCreate) -> Product:
        Category.get_by_id(db, product_data.category_id)
        
        if product_data.barcode is not None:
            self._validate_ean13(product_data.barcode)
        
        sku = product_data.sku or generate_sku()
        
        data = product_data.model_copy(
            update={"sku": sku}
        )
        
        try:
            return self.product_database.create_product(db, data)
        except IntegrityError as e:
            raise DuplicateException("The SKU or barcode already exists") from e
    
    def get_product_by_id(self, db: Session, product_id: UUID) -> Product:
        return self.product_database.get_product(db, product_id)
    
    def list_products(self, db: Session, category_id: UUID | None = None, skip: int = 0, limit = 50) -> list[Product]:
        return self.product_database.list_products(db, category_id, skip, limit)
    
    def update_product(self, db: Session, product_id: UUID, update_data: ProductUpdate) -> Product:
        product = self.product_database.get_product(db, product_id)
        
        updated = update_data.model_dump(exclude_unset=True)
        
        if "category_id" in updated:
            Category.get_category(db, updated["category_id"])

        if "barcode" in updated and updated["barcode"]:
            self._validate_ean13(updated["barcode"])

        return ProductDatabase.update_product(
            db,
            product.product_id,
            update_data,
        )
    
    def delete_product_by_id(self, db: Session, product_id: UUID):
        product = self.product_database.get_product(db, product_id)
        
        if product.product_id is None:
            raise ProductNotFoundException("Product not existing")
        
        return self.product_database.delete_product(db, product_id)
    
    def _validate_ean13(self, barcode: str) -> None:
            if len(barcode) != 13 or not barcode.isdigit():
                raise InvalidBarcodeException("Barcode must be a 13-digit EAN-13 barcode")
            
            digits = [int(digit) for digit in barcode]
            
            checksum = sum(
                digit if index % 2 == 0 else digit * 3
                for index, digit in enumerate(digits[:12])
            )
    
            expected_check_digit = (10 - checksum % 10) % 10
    
            if digits[-1] != expected_check_digit:
                raise InvalidBarcodeException("Invalid EAN-13 check digit")