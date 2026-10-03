import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.forza_backend.core.exceptions import (
    DatabaseException,
    DuplicateException,
    SupplierInActiveException,
    SupplierNotFoundException,
)
from src.forza_backend.infrastructure.database.models.supplier import Supplier
from src.forza_backend.infrastructure.database.models.inventory import Inventory
from src.forza_backend.schemas.supplier import SupplierCreate, SupplierUpdate
from src.forza_backend.services.supplier import SupplierService
from src.tests.database.utils.mock_data import mock_supplier


@pytest.fixture
def db_session():
    return MagicMock()


# --- Model Unit Tests ---

def test_get_by_id_success(db_session: MagicMock):
    supplier_id = uuid4()

    mock_session = MagicMock()
    mock_session.supplier_id = supplier_id
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_session

    result = Supplier.get_by_id(db_session, supplier_id)

    assert result.supplier_id == supplier_id
    db_session.query.assert_called_once_with(Supplier)


def test_get_by_id_raise_not_found(db_session: MagicMock):
    supplier_id = uuid4()

    db_session.query.return_value.filter.return_value.one_or_none.return_value = None

    with pytest.raises(SupplierNotFoundException, match="Supplier not found"):
        Supplier.get_by_id(db_session, supplier_id)


# --- Service Unit Tests ---

def test_service_create_supplier_success(db_session: MagicMock):
    data = SupplierCreate(
        supplier_name="Acme Corp",
        contact_name="Alice",
        email="alice@acme.com",
        phone="1234567890",
        address="123 Main St",
    )

    created = SupplierService.create_supplier(db_session, data)

    assert created.supplier_name == "Acme Corp"
    assert created.contact_name == "Alice"
    db_session.add.assert_called_once()
    db_session.flush.assert_called_once()
    db_session.refresh.assert_called_once()


def test_service_create_supplier_duplicate_raises(db_session: MagicMock):
    data = SupplierCreate(supplier_name="Acme Corp")
    db_session.flush.side_effect = IntegrityError("statement", "params", Exception("duplicate"))

    with pytest.raises(DuplicateException, match="This supplier already exists"):
        SupplierService.create_supplier(db_session, data)

    db_session.rollback.assert_called_once()


def test_service_get_supplier_success(db_session: MagicMock):
    supplier_id = uuid4()
    mock_item = MagicMock()
    mock_item.supplier_id = supplier_id
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_item

    result = SupplierService.get_supplier(db_session, supplier_id)

    assert result.supplier_id == supplier_id


def test_service_list_suppliers(db_session: MagicMock):
    mock_list = [MagicMock(), MagicMock()]
    (
        db_session.query.return_value
        .order_by.return_value
        .offset.return_value
        .limit.return_value
        .all.return_value
    ) = mock_list

    result = SupplierService.list_suppliers(db_session, skip=0, limit=10)

    assert len(result) == 2


def test_service_update_supplier_success(db_session: MagicMock):
    supplier_id = uuid4()
    mock_instance = MagicMock()
    mock_instance.supplier_id = supplier_id
    mock_instance.supplier_name = "Old Name"
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_instance

    data = SupplierUpdate(supplier_name="New Name")
    result = SupplierService.update_supplier(db_session, supplier_id, data)

    assert result.supplier_name == "New Name"
    db_session.flush.assert_called_once()
    db_session.refresh.assert_called_once()


def test_service_delete_supplier_success(db_session: MagicMock):
    supplier_id = uuid4()
    mock_instance = MagicMock()
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_instance

    SupplierService.delete_supplier(db_session, supplier_id)

    db_session.delete.assert_called_once_with(mock_instance)
    db_session.flush.assert_called_once()


def test_service_delete_supplier_with_associated_records(db_session: MagicMock):
    supplier_id = uuid4()
    mock_instance = MagicMock()
    db_session.query.return_value.filter.return_value.one_or_none.return_value = mock_instance
    db_session.flush.side_effect = IntegrityError("statement", "params", Exception("foreign key"))

    with pytest.raises(SupplierInActiveException, match="Cannot delete a supplier that still has purchase orders"):
        SupplierService.delete_supplier(db_session, supplier_id)

    db_session.rollback.assert_called_once()


# --- Integration Tests ---

def test_get_by_id_success_integration(test_session: Session):
    supplier = mock_supplier()

    test_session.add(supplier)
    test_session.commit()

    result = Supplier.get_by_id(test_session, supplier.supplier_id)

    assert supplier.supplier_id == result.supplier_id


def test_get_by_id_raises_not_found_integration(test_session: Session):
    with pytest.raises(SupplierNotFoundException, match="Supplier not found"):
        Supplier.get_by_id(test_session, uuid4())
