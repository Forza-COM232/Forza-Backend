from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from ...schemas.supplier import SupplierCreate, SupplierUpdate
from .models.supplier import Supplier
from ...core.exceptions import DuplicateException, DatabaseException

class SupplierDatabase():
    @staticmethod
    def create_supplier(db: Session, supplier_data: SupplierCreate):
        supplier = Supplier(**supplier_data.model_dump())
        db.add(supplier)
        
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to create supplier.") from e
        db.refresh(supplier)
        return supplier
    
    @staticmethod
    def get_supplier_by_id(db: Session, supplier_id: UUID) -> Supplier:
        return Supplier.get_by_id(db, supplier_id)
    
    @staticmethod
    def list_suppliers(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> list[Supplier]:
        return db.query(Supplier).order_by(Supplier.supplier_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_supplier(db: Session, supplier_id: UUID, supplier_data: SupplierUpdate) -> Supplier:
        supplier = Supplier.get_by_id(db, supplier_id)
        
        data_changes = supplier_data.model_dump(exclude_unset=True)
        for field, value in data_changes.items():
            setattr(supplier, field, value)
        
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DuplicateException("Supplier already exists.") from e
        except Exception as e:
            raise DatabaseException("Failed to update supplier") from e
        db.refresh(supplier)
        return supplier
    
    @staticmethod
    def delete_supplier(db: Session, supplier_id: UUID) -> None:
        supplier = Supplier.get_by_id(db, supplier_id)
        
        try:
            db.delete(supplier)
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to delete supplier") from e
