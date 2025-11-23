import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User, Project, Summary
from database import Base, engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OSS Backend API with Claude")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth import router as auth_router
from projects import router as project_router
from summarize import router as summary_router

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(summary_router, prefix="/projects", tags=["Summaries"])

@app.get("/")
def root():
    logging.info("Root API called")
    return {"message": "OSS Backend API Running"}
