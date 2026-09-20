import pytest
from uuid import uuid4
from sqlalchemy.orm import Session

from src.forza_backend.infrastructure.database.models.users import User
from src.forza_backend.core.exceptions import NotFoundException, UserNotFoundException

def test_get_by_id_raises_not_found_when_missing(test_session: Session):
    with pytest.raises(NotFoundException, match="User not found"):
        User.get_by_id(test_session, uuid4())

def test_get_by_email_raises_not_found_when_no_users_found(test_session: Session):
    non_existent_email = "test@email.com"
    with pytest.raises(UserNotFoundException, match="No user found with that email"):
        User.get_by_email(test_session, non_existent_email)