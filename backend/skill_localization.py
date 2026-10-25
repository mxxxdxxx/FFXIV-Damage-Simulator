
"""
FFXIV 기술 한국어 명칭 매핑 모듈.

Action ID와 패치 버전을 기준으로
공식 한국어 기술명을 조회한다.

한국어 이름이 등록되지 않은 경우 None을 반환한다.
"""

import json
import re

from functools import lru_cache
from pathlib import Path


# ============================================================
# 1. 한국어 기술명 데이터 경로
# ============================================================

LOCALIZATION_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "localization"
)


# ============================================================
# 2. 패치별 한국어 기술명 로드
# ============================================================

@lru_cache(maxsize=32)
def load_korean_skill_names(patch: str) -> dict[str, str]:
    """
    지정한 패치의 한국어 기술명 매핑 데이터를 로드한다.

    예:
        patch = "7.57"

    파일이 없으면 빈 딕셔너리를 반환한다.
    잘못된 파일 구조는 오류로 처리한다.
    """

    # 패치 문자열 검증
    if not re.fullmatch(r"\d+\.\d{1,2}", patch):
        raise ValueError(
            f"잘못된 패치 버전 형식입니다: {patch}"
        )

    # 예: ko_7.57.json
    file_path = LOCALIZATION_DIR / f"ko_{patch}.json"

    # 해당 패치의 한국어 매핑 파일이 없는 경우
    if not file_path.is_file():
        return {}

    # JSON 파일 읽기
    data = json.loads(
        file_path.read_text(encoding="utf-8")
    )

    # 데이터 구조 검증
    if not isinstance(data, dict):
        raise ValueError("한국어 매핑 데이터 형식이 잘못되었습니다.")

    if data.get("patch") != patch:
        raise ValueError("매핑 파일의 패치 정보가 일치하지 않습니다.")

    names = data.get("names")

    if not isinstance(names, dict):
        raise ValueError("한국어 기술명 목록이 없습니다.")

    # 매핑된 기술명 검증
    for action_id, name_ko in names.items():
        if not (
            isinstance(action_id, str)
            and action_id.isdecimal()
            and isinstance(name_ko, str)
            and name_ko.strip()
        ):
            raise ValueError(
                f"잘못된 한국어 기술명 데이터: {action_id}"
            )

    return names


# ============================================================
# 3. Action ID 기반 한국어 기술명 조회
# ============================================================

def get_korean_skill_name(
    action_id: int | str,
    *,
    patch: str,
) -> str | None:
    """
    Action ID에 해당하는 한국어 기술명을 반환한다.

    예:
        get_korean_skill_name(75, patch="7.57")
        → "직선 찌르기"

    등록되지 않은 기술은 None을 반환한다.
    """

    names = load_korean_skill_names(patch)

    return names.get(str(action_id))
