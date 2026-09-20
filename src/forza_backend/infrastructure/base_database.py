from typing import Any, Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, DeclarativeBase
from ..core.exceptions import DatabaseException, DuplicateException, NotFoundException

class Base(DeclarativeBase):
    ...

ModelType = TypeVar("ModelType", bound=Base)

class BaseDatabase(Generic[ModelType]):
    """
    Generic SQLAlchemy ORM repository base class for a single table.

    A subclass sets `model` to the mapped ORM class it operates on; the
    session is provided by the caller at construction time (typically via
    a FastAPI dependency) rather than owned by the repo, so the caller
    controls the transaction boundary — this class only flushes, never
    commits. Writes (`create`, `update`, `delete`) run inside a SAVEPOINT
    via `Session.begin_nested()`, so a failure in one call rolls back only
    that call's change, leaving any other pending work in the session
    (e.g. an earlier repo call in the same request) intact.

    Type Parameters:
        ModelType: The SQLAlchemy declarative model mapped to a table.

    Attributes:
        model (Type[ModelType]): The ORM class this repo operates on.
                                  Must be set on the subclass.

    Example:
        ```python
        class UserDatabase(BaseDatabase[User]):
            model = User

        # in a route, with `db: Session = Depends(get_db)`:
        user_db = UserDatabase(db)
        user = user_db.get(user_id=user_id)
        ```

    Raises:
        ValueError: If `model` is not set on the subclass.
    """
    
    model: Type[ModelType]
    
    def __init__(self, db: Session) -> None:
        if not hasattr(self, "model"):
            raise ValueError("Model must be define")
        
        self.db = db
    
    def create(self, item: ModelType) -> ModelType:
        """
        Insert a new row.

        Runs inside a SAVEPOINT: on failure, only this insert is rolled
        back, not the rest of the session's pending work.

        Args:
            item (ModelType): The Pydantic model instance to insert.

        Raises:
            DuplicateException: if data violates unique constraints
            DatabaseException: if any other database error occurs

        Returns:
            ModelType: The inserted row
        """
        
        try:
            with self.db.begin_nested():
                self.db.add(item)
                self.db.flush()
                
            self.db.refresh(item)
            return item
        except IntegrityError as e:
            raise DuplicateException from e
        except SQLAlchemyError as e:
            raise DatabaseException from e
    
    def get(self, **filters: Any) -> ModelType:
        """
        Retrieve a single row matching the given filters.
        
        

        Raises:
            NotFoundException: If no row matches the filters.
            DatabaseException: If a database error occurs (including one
                                surfaced via autoflush of prior pending
                                changes in this session).

        Returns:
            ModelType: The first matching row.
        """
        
        try:
            statement = select(self.model).filter_by(**filters)
            result = self.db.execute(statement)
            item = result.scalars().first()
            
            if item is None:
                raise NotFoundException(
                    f"{self.model.__name__} not found"
                    f"Filters: {filters}"
                )
            
            return item
        
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException from e
    
    def get_many(self, **filters: Any) -> list[ModelType]:
        """
        Retrieve all rows matching the given filters.

        Raises:
            DatabaseException: If a database error occurs.

        Returns:
            list[ModelType]: Matching rows, or an empty list if none match.
        """
        
        try:
            statement = select(self.model).filter_by(**filters)
            result = self.db.execute(statement)
            return list(result.scalars().all())
        
        except SQLAlchemyError as e:
            raise DatabaseException from e
    
    def update(self, item: ModelType, **values: Any) -> ModelType:
        """
        Apply field updates to an already-fetched row.
        
        Runs inside a SAVEPOINT: on failure, only this update is rolled
        back, not the rest of the session's pending work.

        Args:
            item (ModelType): A row already loaded in this session
            **values: The identified row to update

        Raises:
            DatabaseException: If a database error occurs, including a
                                unique constraint violation

        Returns:
            ModelType: The updated row
        """
        
        try:
            with self.db.begin_nested():
                for field, value in values.items():
                    setattr(item, field, value)
                self.db.flush()
                
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            raise DatabaseException from e
    
    def delete(self, item: ModelType) -> bool:
        """
        Delete an already-fetched row.

        Runs inside a SAVEPOINT: on failure, only this delete is rolled
        back, not the rest of the session's pending work.

        Args:
            item (ModelType): A row already loaded in this session

        Raises:
            DatabaseException: If any other database error occurs.

        Returns:
            bool: True if the delete succeeded.
        """
        
        try:
            with self.db.begin_nested():
                self.db.delete(item)
                self.db.flush()
            return True
        except SQLAlchemyError as e:
            raise DatabaseException from e