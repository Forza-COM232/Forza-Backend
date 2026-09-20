from sqlalchemy import Integer, String, Engine
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.forza_backend.infrastructure.database import connection
from src.forza_backend.infrastructure.database.connection import Base

class TestModel(Base):
    __tablename__ = "test_model"
    
    test_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(String)

def test_raw_session_add_and_persists_model(test_session: Session):
    """Test that explicit session operations persist a new model."""
    model = TestModel(name="Test")
    
    test_session.add(model)
    test_session.flush()
    
    assert model.test_id is not None
    test_session.commit()
    
    retrieved_name = test_session.query(TestModel).filter_by(name="Test").one()
    assert retrieved_name.name == "Test"

def test_raw_session_delete_removes_from_database(test_session: Session):
    """Test that explicit session delete removes a model."""
    model = TestModel(name="To Delete")
    test_session.add(model)
    test_session.commit()
    model_id = model.test_id

    test_session.delete(model)
    test_session.flush()
    test_session.commit()

    result = test_session.query(TestModel).filter_by(test_id=model_id).one_or_none()
    assert result is None


def test_raw_session_flush_applies_updates(test_session: Session):
    """Test that explicit flush makes pending changes visible before commit."""
    model = TestModel(name="Before")
    test_session.add(model)
    test_session.commit()

    model.name = "After"
    test_session.flush()

    refreshed = test_session.query(TestModel).filter_by(test_id=model.test_id).one()
    assert refreshed.name == "After"


def test_get_session_closes_after_context_exit(test_engine: Engine):
    """Test that get_db closes the session after use."""
    from unittest.mock import patch, MagicMock

    mock_session = MagicMock()

    with patch(
        "src.forza_backend.infrastructure.database.connection.SessionLocal",
        return_value=mock_session,
    ):
        gen = connection.get_db()
        session = next(gen)

        assert session is mock_session

        try:
            next(gen)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()