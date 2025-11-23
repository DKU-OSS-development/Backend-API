# OSS Project Backend API  
FastAPI + SQLite + Anthropic Claude + Docker

This project is a backend API server for OSS project analysis and summarization automation.

## Features
- JWT Authentication
- Project Creation & Listing
- File Upload (PDF/TXT/DOCX)
- PDF Parsing
- Claude AI Summarization
- Docker Deployment

## Requirements
- Python 3.11+
- Docker Desktop
- Virtual Environment (recommended)

## Project Structure
```
backend/
│── main.py
│── auth.py
│── projects.py
│── summarize.py
│── claude_client.py
│── database.py
│── models.py
│── utils.py
│── requirements.txt
│── README.md
│── .env
│── oss.db
```

## Environment Variables (.env)
```
SECRET_KEY="your_secret"
CLAUDE_API_KEY="sk-ant-..."
```

## Running Locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API Docs:
```
http://localhost:8000/docs
```

## Docker Deployment
### Build
```bash
docker build -t oss-backend .
```

### Run
```bash
docker run -d -p 8000:8000 --env-file .env oss-backend
```

## API Flow
1. Signup
2. Login → Get JWT
3. Create Project with token
4. Upload file to summarize
5. Claude generates summary
6. Summary saved to DB

## Volume Option (SQLite Persistence)
```bash
docker run -d -p 8000:8000 --env-file .env -v ./db:/app/db oss-backend
```

## Example API Calls

### Signup
```
POST /auth/signup
{
  "email": "test@example.com",
  "password": "1234"
}
```

### Login
`POST /auth/login`

### Create Project
`POST /projects/create?token=JWT`

### Summarize
`multipart/form-data` with:
- token
- file
- text (optional)


