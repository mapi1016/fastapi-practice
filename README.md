# FastAPI 게시판 CRUD

Pydantic 유효성 검사, Controller-Service-Repository 3계층 구조,
SQLAlchemy ORM을 사용한 학습용 게시판 API입니다.

## 구조

```text
app/
├── controllers/          # HTTP 요청/응답
├── services/             # 비즈니스 로직
├── repositories/         # DB 조회/저장
├── models/               # SQLAlchemy ORM 모델
├── schemas/              # Pydantic 요청/응답 모델
├── core/database.py      # DB 연결과 세션
└── main.py               # FastAPI 앱 생성
```

요청 흐름은 `Controller -> Service -> Repository -> Database`입니다.

## 실행

Python 3.10 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- 기본 DB: 프로젝트 루트의 `board.db` (SQLite)

다른 DB를 쓰려면 실행 전에 SQLAlchemy 연결 문자열을 지정합니다.

```bash
export DATABASE_URL="postgresql+psycopg://user:password@localhost/board"
```

PostgreSQL 드라이버 등 해당 DB의 드라이버는 별도로 설치해야 합니다.

## API

| Method | URL | 설명 |
|---|---|---|
| POST | `/api/posts` | 게시글 생성 |
| GET | `/api/posts?page=1&size=10` | 게시글 목록 |
| GET | `/api/posts/{post_id}` | 게시글 상세 |
| PATCH | `/api/posts/{post_id}` | 게시글 일부 수정 |
| DELETE | `/api/posts/{post_id}` | 게시글 삭제 |

생성 요청 예시:

```json
{
  "title": "FastAPI 시작",
  "content": "첫 게시글입니다.",
  "author": "mapi"
}
```

제목은 1~100자, 내용은 1~2000자, 작성자는 1~50자이며 앞뒤 공백을
제거한 뒤 검증합니다. 수정 요청에는 최소 한 필드가 필요합니다.

## 테스트

```bash
pytest -q
```
