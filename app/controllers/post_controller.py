from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostListResponse, PostResponse, PostUpdate
from app.services.post_service import PostService


router = APIRouter(prefix="/posts", tags=["posts"])
service = PostService(PostRepository())
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: DbSession) -> object:
    return service.create_post(db, post_data)


@router.get("", response_model=PostListResponse)
def get_posts(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> object:
    return service.get_posts(db, page=page, size=size)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: DbSession) -> object:
    return service.get_post(db, post_id)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostUpdate, db: DbSession) -> object:
    return service.update_post(db, post_id, post_data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: DbSession) -> Response:
    service.delete_post(db, post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

