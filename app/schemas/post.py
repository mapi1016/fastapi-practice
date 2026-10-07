from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator


Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Content = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
Author = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class PostCreate(BaseModel):
    title: Title
    content: Content
    author: Author


class PostUpdate(BaseModel):
    title: Title | None = None
    content: Content | None = None
    author: Author | None = None

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "PostUpdate":
        if not self.model_fields_set:
            raise ValueError("수정할 필드를 하나 이상 입력해야 합니다.")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("수정할 필드에는 null을 입력할 수 없습니다.")
        return self


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int = Field(ge=0)
