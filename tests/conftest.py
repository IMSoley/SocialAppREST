# special file for pytest for fixture, all of the fixture will be available in the test function
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic import command
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # run code before we run our tests
    # command.upgrade("head")
    yield TestClient(app)
    # command.downgrade("base")
    # run code after we run our tests


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture(scope="function")
def test_user_2(client):
    user_data = {"email": "hello123444@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

# for posts
@pytest.fixture(scope="function")
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture(scope="function")
def test_posts(test_user, session, test_user_2):
    posts_data = [
        {"title": "Hello", "content": "Hello World", "owner_id": test_user["id"]},
        {"title": "Hello2", "content": "Hello World2", "owner_id": test_user["id"]},
        {"title": "Hello3", "content": "Hello World3", "owner_id": test_user["id"]},
        {"title": "Hello4", "content": "Hello World4", "owner_id": test_user_2["id"]}
    ]
    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    posts = session.query(models.Post).all()
    return posts
