import pytest
from uuid import uuid4
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.forza_backend.core.enums.movement_types import MovementType
from src.forza_backend.infrastructure.database.models.stock_movement import StockMovement
# from src.forza_backend.infrastructure.database.models.users import User
from src.forza_backend.core.exceptions import StockMovementNotFoundException

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

# Will fail since Product Model haven't implemented yet
def test_get_by_id_success_integration(test_session: Session):
    stock_movement = StockMovement(
        product_id=uuid4(),
        performed_by=uuid4(),
        movement_type=MovementType.STOCK_IN,
        quantity=5,
        reason="Initial stock"
    )
    
    test_session.add(stock_movement)
    test_session.commit()
    
    result = StockMovement.get_by_id(test_session, stock_movement.stock_movement_id)
    
    assert stock_movement.stock_movement_id == result.stock_movement_id