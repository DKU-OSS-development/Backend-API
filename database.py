'''
## 🔧 변경 사항
쿠버네티스 환경에서 데이터가 유실되지 않도록 PVC(영구 스토리지)를 연결하기 위해 database.py 설정을 수정했습니다.

## 📝 상세 내용
- 기존: `sqlite:///./oss.db` (현재 폴더에 저장)
- 변경: `/app/data` 폴더 유무를 확인하여, 쿠버네티스 환경에서는 볼륨 마운트 경로(`/app/data`)에 저장하고, 로컬 개발 환경에서는 기존처럼 현재 폴더에 저장하도록 로직을 개선했습니다.

## ✅ 영향 범위
- 이 코드는 **로컬 개발 환경(내 노트북)에서도 정상 작동**합니다. (폴더가 없으면 자동으로 생성하거나 현재 경로를 사용하도록 예외 처리함)
- 별도의 설정 없이 평소처럼 실행하면 됩니다.

'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 데이터 저장 폴더 지정 (컨테이너 내부 경로)
DB_DIR = "/app/data"

# 로컬 테스트를 위해 폴더가 없으면 생성
if not os.path.exists(DB_DIR):
    try:
        os.makedirs(DB_DIR)
    except OSError:
        # 로컬(Windows) 등 권한 문제나 경로 차이 대비
        DB_DIR = "."

# DB 파일 경로 설정
DATABASE_URL = f"sqlite:///{DB_DIR}/oss.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
