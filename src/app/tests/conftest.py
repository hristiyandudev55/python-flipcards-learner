import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest.mock as mock

from app.main import app
from app.models import Base
from app.tests.database_test import override_get_db, TEST_DATABASE_URL
from app.database import get_db

# Create test database engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Returns a database session for testing"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def mock_s3_logger():
    """Mock S3 logger to prevent errors during testing"""
    with mock.patch('app.utils.s3_logger.s3_logger.log_action') as mock_log:
        mock_log.return_value = None
        yield mock_log
