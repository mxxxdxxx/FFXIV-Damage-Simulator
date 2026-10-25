
"""
XIVAPI v2 용기사 기술 조회 실험.

실행:
    python scripts/xivapi_probe.py

실제 기술 데이터를 저장하거나 Skill 모델로 변환하지 않는다.
API 응답 구조를 확인하는 조사용 스크립트다.
"""

import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# ============================================================
# 1. XIVAPI 기본 설정
# ============================================================

BASE_URL = "https://v2.xivapi.com/api"
GAME_VERSION = "7.57"

# 실험 대상: 용기사 기술
ACTION_IDS = {
    "True Thrust": 75,
    "Vorpal Thrust": 78,
}


# ============================================================
# 2. 요청 URL 생성
# ============================================================

def build_action_url(
    action_id: int,
    version: str = GAME_VERSION,
) -> str:
    """
    Action 시트의 특정 기술을 조회하기 위한 URL 생성.
    """

    params = {
        "fields": "Name,ClassJobLevel,Recast100ms,Icon",
        "transient": "Description",
        "version": version,
        "language": "en",
    }

    query_string = urlencode(params)

    return (
        f"{BASE_URL}/sheet/Action/{action_id}"
        f"?{query_string}"
    )


# ============================================================
# 3. XIVAPI 실제 호출
# ============================================================

def fetch_action(
    action_id: int,
    version: str = GAME_VERSION,
) -> dict:
    """
    XIVAPI에서 기술 데이터를 조회한다.
    """

    # url = build_action_url(action_id, version)
    #
    # with urlopen(url, timeout=15) as response:
    #     data = json.load(response)

    """
    REQUEST 객체로 전달 + HTTP 요청 헤더 명시 -> urlopen()에 전달
    """

    url = build_action_url(action_id, version)

    # 요청 헤더 명시
    request = Request(
        url,
        headers={
            # 서버에 요청을 보내는 클라이언트 + 응답 형식 명시
            "User-Agent": "FFXIV-Damage-Simulator/0.1",
            "Accept": "application/json",
        }
    )

    with urlopen(request, timeout=15) as response:
        data = json.load(response)

    if not isinstance(data, dict):
        raise ValueError("JSON 응답이 객체 형식이 아닙니다.")

    if not isinstance(data.get("fields"), dict):
        raise ValueError("Action fields가 없습니다.")

    return data


# ============================================================
# 4. 주요 필드 추출
# ============================================================

def summarize_action(data: dict) -> dict:
    """
    XIVAPI 응답에서 조사할 필드를 추출한다.

    아직 Skill 모델로 변환하지 않는다.
    """

    fields = data["fields"]

    recast_raw = fields.get("Recast100ms")

    # 100ms = 0.1초
    recast_seconds = (
        recast_raw / 10
        if isinstance(recast_raw, (int, float))
        and not isinstance(recast_raw, bool)
        else None
    )

    transient = data.get("transient") or {}

    return {
        "action_id": data.get("row_id"),
        "name": fields.get("Name"),
        "required_level": fields.get("ClassJobLevel"),
        "recast_raw": recast_raw,
        "recast_seconds": recast_seconds,
        "icon": fields.get("Icon"),
        "description": transient.get("Description"),
        "version": data.get("version"),
        "schema": data.get("schema"),
    }


# ============================================================
# 5. 스크립트 실행
# ============================================================

def main():
    print("=" * 50)
    print("XIVAPI v2 용기사 기술 데이터 조사")
    print(f"요청 게임 버전: {GAME_VERSION}")
    print("=" * 50)

    for action_name, action_id in ACTION_IDS.items():
        print(f"\n조회 대상: {action_name} ({action_id})")

        try:
            raw_data = fetch_action(action_id)
            summary = summarize_action(raw_data)

        except (URLError, ValueError) as exc:
            print(f"조회 실패: {exc}")
            raise SystemExit(1) from exc

        print(
            json.dumps(
                summary,
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
