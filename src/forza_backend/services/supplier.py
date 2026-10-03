from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.exceptions import (
    DatabaseException,
    DuplicateException,
    SupplierInActiveException,
)
from ..infrastructure.database.models.supplier import Supplier
from ..schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:

    @staticmethod
    def create_supplier(db: Session, data: SupplierCreate) -> Supplier:
        supplier = Supplier(**data.model_dump())
        db.add(supplier)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise DuplicateException("This supplier already exists") from exc
        db.refresh(supplier)
        return supplier

    @staticmethod
    def get_supplier(db: Session, supplier_id: UUID) -> Supplier:
        return Supplier.get_by_id(db, supplier_id)

    @staticmethod
    def list_suppliers(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Supplier]:
        return (
            db.query(Supplier)
            .order_by(Supplier.supplier_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_supplier(db: Session, supplier_id: UUID, data: SupplierUpdate) -> Supplier:
        supplier = Supplier.get_by_id(db, supplier_id)

        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(supplier, field, value)

        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise DuplicateException("This supplier already exists") from exc
        db.refresh(supplier)
        return supplier

    @staticmethod
    def delete_supplier(db: Session, supplier_id: UUID) -> None:
        supplier = Supplier.get_by_id(db, supplier_id)
        db.delete(supplier)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise SupplierInActiveException(
                "Cannot delete a supplier that still has purchase orders"
            ) from exc
