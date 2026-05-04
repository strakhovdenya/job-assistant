import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://job_assistant:job_assistant@localhost:5432/job_assistant",
)


# --- ENGINE (один на все тесты) ---
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


# --- DB FIXTURE ---
@pytest.fixture
def db() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# --- OVERRIDE get_db ---
@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()