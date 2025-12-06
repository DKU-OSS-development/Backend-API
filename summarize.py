import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import decode_jwt
from database import SessionLocal
from models import Summary, Project
from file_parser import parse_pdf, parse_txt, parse_docx
from claude_client import call_claude_api

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id_from_token(token: str):
    return decode_jwt(token)["user_id"]

# 기존 요약 생성 API
@router.post("/{project_id}/summarize")
async def summarize(
    project_id: int,
    token: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logging.info(f"[Summarize] 호출됨 project_id={project_id}")

    user_id = get_user_id_from_token(token)
    logging.info(f"[Summarize] 사용자 인증됨 user_id={user_id}")

    # 프로젝트 권한 확인
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(404, "프로젝트를 찾을 수 없거나 권한이 없습니다")

    # 텍스트 or 파일 여부 확인
    if not text and not file:
        raise HTTPException(400, "텍스트 또는 파일 중 하나는 제공해야 함")

    # 파일 업로드 처리
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

    # Claude 요약 실행
    summary_text = call_claude_api(content)

    # DB 저장
    new_summary = Summary(
        project_id=project_id,
        original_text=content[:5000],
        summary=summary_text
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    logging.info(f"[Summarize] 요약 저장 완료 summary_id={new_summary.id}")

    return {
        "summary_id": new_summary.id,
        "summary": summary_text,
        "project_id": project_id,
        "created_at": new_summary.created_at
    }


# ✅ 프로젝트별 요약 목록 조회 API (추가 필요!)
@router.get("/{project_id}/summaries")
def get_project_summaries(
    project_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    user_id = get_user_id_from_token(token)
    
    # 프로젝트 권한 확인
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(404, "프로젝트를 찾을 수 없거나 권한이 없습니다")
    
    # 요약 목록 조회 (최신순)
    summaries = db.query(Summary).filter(
        Summary.project_id == project_id
    ).order_by(Summary.created_at.desc()).all()
    
    return {
        "project_name": project.name,
        "summaries": [
            {
                "id": s.id,
                "summary": s.summary,
                "original_text_preview": s.original_text[:200] if s.original_text else None,
                "created_at": s.created_at
            }
            for s in summaries
        ]
    }


# ✅ 개별 요약 상세 조회 API (추가 필요!)
@router.get("/summary/{summary_id}")
def get_summary_detail(
    summary_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    user_id = get_user_id_from_token(token)
    
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    
    if not summary:
        raise HTTPException(404, "요약을 찾을 수 없습니다")
    
    # 프로젝트 소유자 확인
    project = db.query(Project).filter(
        Project.id == summary.project_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(403, "권한이 없습니다")
    
    return {
        "id": summary.id,
        "project_name": project.name,
        "original_text": summary.original_text,
        "summary": summary.summary,
        "created_at": summary.created_at
    }