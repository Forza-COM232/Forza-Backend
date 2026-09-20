import pytest
from uuid import uuid4
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.forza_backend.core.enums.movement_types import MovementType
from src.forza_backend.infrastructure.database.models.stock_movement import StockMovement
from src.forza_backend.core.exceptions import StockMovementNotFoundException
from src.tests.database.utils.mock_data import mock_product, mock_user

@pytest.fixture
def db_session():
    return MagicMock()

def test_get_by_id_success(db_session: MagicMock):
    stock_movement_id = uuid4()
    
    mock_session = MagicMock()
    mock_session.stock_movement_id = stock_movement_id
    
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_session
    
    result = StockMovement.get_by_id(db_session, stock_movement_id)
    
    assert result.stock_movement_id == stock_movement_id
    db_session.query.assert_called_once_with(StockMovement)

def test_get_by_id_raises_not_found(db_session: MagicMock):
    stock_movement_id = uuid4()
    
    db_session.query.return_value.filter.return_value.one_or_none.return_value = None
    
    with pytest.raises(StockMovementNotFoundException, match="Stock Movement not found"):
        StockMovement.get_by_id(db_session, stock_movement_id)

def test_get_by_id_success_integration(test_session: Session):
    user = mock_user()
    product = mock_product()
    
    stock_movement = StockMovement(
        product_id=product.product_id,
        performed_by=user.user_id,
        movement_type=MovementType.STOCK_IN,
        quantity=5,
        reason="Initial stock"
    )
    
    test_session.add(stock_movement)
    test_session.commit()
    
    result = StockMovement.get_by_id(test_session, stock_movement.stock_movement_id)
    
    assert stock_movement.stock_movement_id == result.stock_movement_id

def test_get_by_id_raises_not_found_integration(test_session: Session):
    with pytest.raises(StockMovementNotFoundException, match="Stock Movement not found"):
        StockMovement.get_by_id(test_session, uuid4())