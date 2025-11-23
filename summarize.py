import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import decode_jwt
from database import SessionLocal
from models import Summary
from file_parser import parse_pdf, parse_txt, parse_docx
from claude_client import call_claude_api

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_uid(token: str):
    return decode_jwt(token)["user_id"]

@router.post("/{project_id}/summarize")
async def summarize(
    project_id: int,
    token: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logging.info(f"[Summarize] 호출됨 project_id={project_id}")

    uid = get_uid(token)
    logging.info(f"[Summarize] 사용자 인증됨 user_id={uid}")

    # 1) 텍스트 or 파일 여부 확인
    if not text and not file:
        raise HTTPException(400, "텍스트 또는 파일 중 하나는 제공해야 함")

    # 2) 파일 업로드 처리
    if file:
        logging.info(f"[File Upload] 파일 수신: {file.filename} ({file.content_type})")

        if file.content_type == "application/pdf":
            content = parse_pdf(file.file)

        elif file.content_type in ["text/plain"]:
            content = parse_txt(file.file)

        elif file.content_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            content = parse_docx(file.file)

        else:
            raise HTTPException(400, "지원하지 않는 파일 형식")

    else:
        content = text
        logging.info(f"[Text Input] 텍스트 길이 {len(text)}")

    # 3) Claude 요약 실행
    summary_text = call_claude_api(content)

    # 4) DB 저장
    s = Summary(
        project_id=project_id,
        original_text=content[:3000],  # 저장 사이즈 제한
        summary=summary_text
    )
    db.add(s)
    db.commit()

    logging.info("[Summarize] 요약 저장 완료")

    return {
        "summary": summary_text,
        "project_id": project_id
    }
