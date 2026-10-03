from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...core.exceptions import CategoryInActiveException
from .models.category import Category
from ...schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def create_category(db: Session, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        db.add(category)
        db.flush()
        db.refresh(category)
        return category

    @staticmethod
    def get_category(db: Session, category_id: UUID) -> Category:
        return Category.get_by_id(db, category_id)

    @staticmethod
    def list_categories(db: Session, skip: int = 0, limit: int = 50,) -> list[Category]:
        return (
            db.query(Category)
            .order_by(Category.category_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_category(db: Session, category_id: UUID, data: CategoryUpdate) -> Category:
        category = Category.get_by_id(db, category_id)
        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(category, field, value)

        db.flush()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: UUID) -> None:
        category = Category.get_by_id(db, category_id)
        db.delete(category)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise CategoryInActiveException(
                "Cannot delete a category that still has products"
            ) from exc