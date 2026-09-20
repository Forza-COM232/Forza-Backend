from uuid import uuid4
from src.forza_backend.core.enums.movement_types import MovementType
from src.forza_backend.core.enums.unit_of_measurements import UnitMeasurements
from src.forza_backend.infrastructure.database.models.users import User
from src.forza_backend.infrastructure.database.models.product import Product
from src.forza_backend.infrastructure.database.models.category import Category
from src.forza_backend.infrastructure.database.models.stock_movement import StockMovement

def mock_user() -> User:
    return User(
        user_id=uuid4(),
        name="Test User",
        email="test@email.com",
        hashed_password="hashed-pass"
    )

def mock_stock_movement() -> StockMovement:
    user = mock_user()
    product = mock_product()
    return StockMovement(
        product_id=product.product_id,
        performed_by=user.user_id,
        movement_type=MovementType.STOCK_IN,
        quantity=5,
        reason="Initial stock"
    )

def mock_product() -> Product:
    category = mock_category()
    return Product(
        product_id=uuid4(),
        category_id=category.category_id,
        sku="NIK-123",
        barcode="ABCC-DEFF",
        product_name="Test Product",
        description="Test",
        unit_measurement=UnitMeasurements.KILOGRAM,
        cost_price=12.00,
        selling_price=15.00,
        reorder_level=20
    )

def mock_category() -> Category:
    return Category(
        category_id=uuid4(),
        category_name="Beverages",
        description="Any drinkable liquids"
    )