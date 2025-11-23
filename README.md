
# 🚀 OSS Backend API (FastAPI + Claude)

본 프로젝트는 **FastAPI 기반 백엔드 API 서버**이며,  
PDF/TXT 파일 업로드 → Claude AI 요약 기능까지 제공하는 경량 백엔드입니다.

---

# ✨ 주요 기능

- 회원가입 / 로그인 (JWT 기반 인증)
- 프로젝트 생성 및 조회
- PDF / TXT 파일 업로드
- Claude API 기반 문서 요약 기능
- SQLite 기반 로컬 데이터 저장
- Swagger UI API 테스트 제공
- Docker 기반 배포 지원

---

# 🧰 기술 스택

- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **SQLite**
- **JWT (PyJWT)**
- **bcrypt**
- **Multipart Upload**
- **Claude API**
- **python-dotenv**
- **Docker**

---

# 📦 설치 방법

```bash
git clone https://github.com/DKU-OSS-development/Backend-API.git
cd Backend-API

# 가상환경 생성 (선택)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

---

# ▶ 서버 실행 (Development)

```bash
uvicorn main:app --reload
```

실행 후 브라우저에서 확인:

- Swagger UI → http://localhost:8000/docs  
- ReDoc → http://localhost:8000/redoc  
- Root API → http://localhost:8000/

---

# 🧪 API Documentation (Swagger)

FastAPI는 자동으로 Swagger UI 기반 API 문서를 제공합니다.

서버 실행 후 아래 주소로 접속하세요:

👉 **Swagger UI:**  
http://localhost:8000/docs

👉 **ReDoc:**  
http://localhost:8000/redoc

Swagger에서는 회원가입, 로그인, 프로젝트 생성, 파일 업로드, 요약 기능까지  
모든 API를 테스트할 수 있습니다.

---

# 🔑 API 엔드포인트 요약

## 📌 Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | 회원가입 |
| POST | `/auth/login` | 로그인 (JWT 발급) |

---

## 📌 Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects/create` | 프로젝트 생성 |
| GET | `/projects` | 내 프로젝트 목록 조회 |

---

## 📌 Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects/{project_id}/summarize` | PDF/TXT 업로드 → Claude 요약 |

---

# 🐳 Docker 배포

Docker를 사용해 쉽게 배포할 수 있습니다.

## 1) 이미지 빌드

```bash
docker build -t oss-backend .
```

## 2) 컨테이너 실행

```bash
docker run -d -p 8000:8000 --name oss-backend-container oss-backend
```

## 3) 확인

브라우저에서:

```
http://localhost:8000/docs
```

---

# 📄 파일 업로드 요약 흐름

1. `/projects/{id}/summarize` 로 요청
2. PDF/TXT File 업로드
3. 서버가 파일을 읽고 텍스트 추출
4. Claude API 호출
5. 요약 결과를 DB에 저장
6. API 응답으로 요약 텍스트 반환

---

# 📁 로컬 DB

SQLite 파일은 자동으로 생성됩니다.

```
oss.db
```

DB는 테이블 자동 생성 스크립트로 초기화됩니다.

---
