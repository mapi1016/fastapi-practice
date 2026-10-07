from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def create(self, db: Session, post_data: PostCreate) -> Post:
        post = Post(**post_data.model_dump())
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def find_all(self, db: Session, *, offset: int, limit: int) -> list[Post]:
        statement = select(Post).order_by(Post.id.desc()).offset(offset).limit(limit)
        return list(db.scalars(statement).all())

    def count(self, db: Session) -> int:
        statement = select(func.count()).select_from(Post)
        return db.scalar(statement) or 0

    def find_by_id(self, db: Session, post_id: int) -> Post | None:
        return db.get(Post, post_id)

    def update(self, db: Session, post: Post, post_data: PostUpdate) -> Post:
        for field, value in post_data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        db.commit()
        db.refresh(post)
        return post

    def delete(self, db: Session, post: Post) -> None:
        db.delete(post)
        db.commit()

