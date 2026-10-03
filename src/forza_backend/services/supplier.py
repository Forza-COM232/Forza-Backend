from uuid import UUID
from sqlalchemy.orm import Session
from ..infrastructure.database.supplier_database import SupplierDatabase
from ..infrastructure.database.models.supplier import Supplier
from ..schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    @staticmethod
    def create_supplier(
        db: Session,
        supplier_data: SupplierCreate,
    ) -> Supplier:
        return SupplierDatabase.create_supplier(db, supplier_data)
    
    @staticmethod
    def get_supplier(
        db: Session,
        supplier_id: UUID,
    ) -> Supplier:

        return SupplierDatabase.get_supplier_by_id(
            db,
            supplier_id,
        )
    
    @staticmethod
    def list_suppliers(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Supplier]:

        return SupplierDatabase.list_suppliers(
            db,
            skip=skip,
            limit=limit,
        )
    
    @staticmethod
    def update_supplier(
        db: Session,
        supplier_id: UUID,
        supplier_data: SupplierUpdate,
    ) -> Supplier:
        SupplierDatabase.get_supplier_by_id(
            db,
            supplier_id,
        )

        return SupplierDatabase.update_supplier(
            db,
            supplier_id,
            supplier_data,
        )
    
    @staticmethod
    def deactivate_supplier(
        db: Session,
        supplier_id: UUID,
    ) -> Supplier:

        supplier = SupplierDatabase.get_supplier_by_id(
            db,
            supplier_id,
        )

        supplier.is_active = False

        db.flush()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def activate_supplier(
        db: Session,
        supplier_id: UUID,
    ) -> Supplier:

        supplier = SupplierDatabase.get_supplier_by_id(
            db,
            supplier_id,
        )

        supplier.is_active = True

        db.flush()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def delete_supplier(
        db: Session,
        supplier_id: UUID,
    ) -> None:

        SupplierDatabase.delete_supplier(
            db,
            supplier_id,
        )