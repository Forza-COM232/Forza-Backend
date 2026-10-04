from uuid import UUID
from sqlalchemy.orm import Session
from ..infrastructure.database.models.users import User
from ..infrastructure.database.user_database import UserDatabase
from ..schemas.user import UserUpdate
from ..core.exceptions import UserAlreadyDeactivatedException

class UserService():
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        return UserDatabase.get_user_by_id(db, user_id)
    
    @staticmethod
    def list_user(db: Session, skip: int = 0, limit: int = 0) -> list[User]:
        return UserDatabase.list_users(db, skip, limit)
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
        user = UserDatabase.get_user_by_id(db, user_id)
        
        user_changes = user_data.model_dump(exclude_unset=True)
        
        for field, value in user_changes.items():
            setattr(user, field, value)
        
        return UserDatabase.update_user(db, user)
    
    @staticmethod
    def deactivate_user(db, user_id: UUID) -> User:
        user = UserDatabase.get_user_by_id(db, user_id)
        
        if not user.is_active:
            raise UserAlreadyDeactivatedException("User already deactivated")

        user.is_active = False
        
        return UserDatabase.update_user(db, user)
    
    @staticmethod
    def activate_user(db: Session, user_id: UUID) -> User:
        user = UserDatabase.get_user_by_id(db, user_id)
        user.is_active = True
        return UserDatabase.update_user(db, user)
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        return UserDatabase.delete_user(db, user_id)