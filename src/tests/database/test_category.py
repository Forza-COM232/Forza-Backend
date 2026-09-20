import pytest
from uuid import uuid4
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.forza_backend.infrastructure.database.models.category import Category
from src.forza_backend.core.exceptions import CategoryNotFoundException
from src.tests.database.utils.mock_data import mock_category

@pytest.fixture
def db_session():
    return MagicMock()

def test_get_by_id_success(db_session: MagicMock):
    category_id = uuid4()
    
    mock_session = MagicMock()
    mock_session.category_id = category_id
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_session
    
    result = Category.get_by_id(db_session, category_id)
    
    assert result.category_id == category_id
    db_session.query.assert_called_once_with(Category)

def test_get_by_id_raise_not_found(db_session: MagicMock):
    category_id = uuid4()
    
    db_session.query.return_value.filter.return_value.one_or_none.return_value = None
    
    with pytest.raises(CategoryNotFoundException, match="Category not found"):
        Category.get_by_id(db_session, category_id)

# Integration Test
def test_get_by_id_success_integration(test_session: Session):
    category = mock_category()
    
    test_session.add(category)
    test_session.commit()
    
    result = Category.get_by_id(test_session, category.category_id)
    
    assert category.category_id == result.category_id

def test_get_by_id_raises_not_found_integration(test_session: Session):
    with pytest.raises(CategoryNotFoundException, match="Category not found"):
        Category.get_by_id(test_session, uuid4())