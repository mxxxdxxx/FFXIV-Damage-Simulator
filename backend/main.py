
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="FFXIV Damage Simulator API",
    description="FFXIV 스킬 로테이션 및 기대 피해량 계산 API",
    version="0.1.0"
)

# Next.js 프론트엔드와 통신하기 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서버 상태 확인 API
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "FFXIV Damage Simulator API is running"
    }
