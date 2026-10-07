import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=test_engine, autoflush=False, expire_on_commit=False
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        with TestingSessionLocal() as db:
            yield db

    app = create_app(initialize_database=False)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_post_crud(client: TestClient) -> None:
    create_response = client.post(
        "/api/posts",
        json={"title": "첫 글", "content": "FastAPI 학습", "author": "mapi"},
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    detail_response = client.get(f"/api/posts/{post_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["title"] == "첫 글"

    list_response = client.get("/api/posts?page=1&size=10")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    update_response = client.patch(
        f"/api/posts/{post_id}", json={"title": "수정한 글"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "수정한 글"

    delete_response = client.delete(f"/api/posts/{post_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/api/posts/{post_id}").status_code == 404


def test_validation_rejects_blank_title(client: TestClient) -> None:
    response = client.post(
        "/api/posts",
        json={"title": "   ", "content": "내용", "author": "작성자"},
    )
    assert response.status_code == 422


def test_update_requires_a_field(client: TestClient) -> None:
    create_response = client.post(
        "/api/posts",
        json={"title": "제목", "content": "내용", "author": "작성자"},
    )
    post_id = create_response.json()["id"]

    response = client.patch(f"/api/posts/{post_id}", json={})
    assert response.status_code == 422

    null_response = client.patch(f"/api/posts/{post_id}", json={"title": None})
    assert null_response.status_code == 422
