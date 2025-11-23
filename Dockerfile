FROM python:3.13-slim

# 시스템 패키지 업데이트
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements 복사 및 설치
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 소스 코드 전체 복사
COPY . .

# 환경 변수 등록 (Docker 내부에서도 .env 사용)
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# uvicorn 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
