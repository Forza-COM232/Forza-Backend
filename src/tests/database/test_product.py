import pytest
from uuid import uuid4
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.forza_backend.infrastructure.database.models.product import Product
from src.forza_backend.core.exceptions import ProductNotFoundException
from src.forza_backend.core.enums.unit_of_measurements import UnitMeasurements

@pytest.fixture
def db_session():
    return MagicMock()

def test_get_by_id_success(db_session: MagicMock):
    product_id = uuid4()
    
    mock_session = MagicMock()
    mock_session.product_id = product_id
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_session
    
    result = Product.get_by_id(db_session, product_id)
    
    assert result.product_id == product_id
    db_session.query.assert_called_once_with(Product)

def test_get_by_id_raise_not_found(db_session: MagicMock):
    product_id = uuid4()
    
    db_session.query.return_value.filter.return_value.one_or_none.return_value = None
    
    with pytest.raises(ProductNotFoundException, match="Product not found"):
        Product.get_by_id(db_session, product_id)

# Integration Test will fail until Category Model has been implemented
def test_get_by_id_success_integration(test_session: Session):
    product = Product(
        product_id=uuid4(),
        category_id=uuid4(),
        sku="NIK-123",
        bardcode="ABCC-DEFF",
        product_name="Test Product",
        description="Test",
        unit_measurement=UnitMeasurements.KILOGRAM,
        cost_price=12.00,
        selling_price=15.00,
        reorder_level=20
    )
    
    test_session.add(product)
    test_session.commit()
    
    result = Product.get_by_id(test_session, product.product_id)
    
    assert product.product_id == result.product_id