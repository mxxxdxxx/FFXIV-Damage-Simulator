
import logging
import re

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from skill_models import SkillDataset


# ============================================================
# 1. 라우터 설정
# ============================================================

router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"]
)

logger = logging.getLogger(__name__)


# ============================================================
# 2. 기술 데이터 경로
# ============================================================

# backend/data/skills/
SKILLS_DATA_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "skills"
)


# ============================================================
# 3. 직업별 기술 조회 API
# ============================================================

@router.get(
    "/{job}",
    response_model=SkillDataset,
    summary="직업별 기술 데이터 조회",
    description=(
        "직업, 레벨, 패치 버전을 기준으로 "
        "기술 데이터셋을 반환합니다."
    )
)
def get_job_skills(
    job: str,
    level: int = Query(..., ge=1),
    patch: str = Query(..., min_length=1)
) -> SkillDataset:

    # -------------------------
    # 직업 코드 정규화 및 검증
    # -------------------------

    # drg → DRG
    job_code = job.upper()

    if not re.fullmatch(r"[A-Z]{3}", job_code):
        raise HTTPException(
            status_code=400,
            detail="직업 코드는 영문 3글자여야 합니다."
        )

    # -------------------------
    # 직업 / 레벨에 맞는 파일 검색
    # -------------------------

    # 예: drg_100_prototype.json
    file_pattern = f"{job_code.lower()}_{level}_*.json"

    matching_files = sorted(
        SKILLS_DATA_DIR.glob(file_pattern)
    )

    # -------------------------
    # JSON 로드 및 데이터 검증
    # -------------------------

    for file_path in matching_files:

        try:
            json_text = file_path.read_text(
                encoding="utf-8"
            )

            dataset = SkillDataset.model_validate_json(
                json_text
            )

        except (OSError, ValidationError) as exc:
            logger.exception(
                "기술 데이터 로드 실패: %s",
                file_path
            )

            raise HTTPException(
                status_code=500,
                detail="기술 데이터 파일을 처리할 수 없습니다."
            ) from exc

        # -------------------------
        # 요청 조건 확인
        # -------------------------

        if (
            dataset.job.upper() == job_code
            and dataset.level == level
            and dataset.patch == patch
        ):
            return dataset

    # -------------------------
    # 해당 데이터가 없을 경우
    # -------------------------

    raise HTTPException(
        status_code=404,
        detail=(
            f"기술 데이터를 찾을 수 없습니다. "
            f"job={job_code}, "
            f"level={level}, "
            f"patch={patch}"
        )
    )
