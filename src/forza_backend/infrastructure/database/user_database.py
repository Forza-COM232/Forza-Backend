from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models.users import User
from ...core.exceptions import DatabaseException

class UserDatabase():
    @staticmethod
    def create_user(db: Session, user: User) -> User:
        db.add(user)
        try:
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to create user.") from e
        db.flush()
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        return User.get_by_id(db, user_id)
    
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 0) -> list[User]:
        return db.query(User).order_by(User.user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        user = User.get_by_id(db, user_id)
        
        try:
            db.delete(user)
            db.flush()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseException("Failed to delete user.") from e
        return True