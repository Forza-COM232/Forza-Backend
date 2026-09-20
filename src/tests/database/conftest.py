import pytest
from typing import Any
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from src.forza_backend.infrastructure.database.connection import Base

def _disable_fk_constraints(dbapi_connection: Any, _connection_record: Any) -> None:
    with dbapi_connection.cursor() as cursor:
        cursor.execute("SET session_replication_role = 'replica';")

@pytest.fixture(scope="session")
def postgres_container():
    """Start a PostgreSQL container for the entire test session."""
    container = PostgresContainer("postgres:18")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="function")
def test_engine(postgres_container: PostgresContainer):
    """
    Create a PostgreSQL engine for testing with JSONB support.
    
    Creates a fresh database for each test.
    """
    connection_url = postgres_container.get_connection_url()
    
    engine = create_engine(connection_url)
    
    event.listen(engine, "connect", _disable_fk_constraints)
    
    Base.metadata.create_all(bind=engine)
    yield engine
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        ...
    
    engine.dispose()

@pytest.fixture(scope="function")
def test_session(test_engine: Engine):
    """Create a new database session for each test."""
    session_factory = sessionmaker(bind=test_engine)
    session = session_factory()
    yield session
    session.close()