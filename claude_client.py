import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# 콘솔에서 쓰는 실제 모델명
CLAUDE_MODEL = "claude-sonnet-4-20250514"

def call_claude_api(text: str) -> str:

    logging.info("[Claude] 호출 시작")
    logging.info(f"[Claude] 요청 텍스트 길이: {len(text)}")

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"   # ✔️ 필수
    }

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1500,
        "messages": [{
            "role": "user",
            "content": f"Summarize the following text:\n\n{text}"
        }]
    }

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )

    logging.info(f"[Claude] 응답 코드: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"[Claude] API Error: {response.text}")
        raise Exception("Claude API Error")

    result = response.json()["content"][0]["text"]
    logging.info("[Claude] 응답 수신 완료")

    return result
