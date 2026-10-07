from sqlalchemy.orm import Session

from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostListResponse, PostUpdate


class PostNotFoundError(Exception):
    def __init__(self, post_id: int) -> None:
        super().__init__(f"게시글 {post_id}을(를) 찾을 수 없습니다.")


class PostService:
    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository

    def create_post(self, db: Session, post_data: PostCreate) -> Post:
        return self.repository.create(db, post_data)

    def get_posts(self, db: Session, *, page: int, size: int) -> PostListResponse:
        offset = (page - 1) * size
        posts = self.repository.find_all(db, offset=offset, limit=size)
        total = self.repository.count(db)
        return PostListResponse(items=posts, total=total)

    def get_post(self, db: Session, post_id: int) -> Post:
        post = self.repository.find_by_id(db, post_id)
        if post is None:
            raise PostNotFoundError(post_id)
        return post

    def update_post(self, db: Session, post_id: int, post_data: PostUpdate) -> Post:
        post = self.get_post(db, post_id)
        return self.repository.update(db, post, post_data)

    def delete_post(self, db: Session, post_id: int) -> None:
        post = self.get_post(db, post_id)
        self.repository.delete(db, post)

