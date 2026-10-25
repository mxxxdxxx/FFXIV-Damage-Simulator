
"""
한국어 FFXIV Action CSV를 JSON 매핑 데이터로 변환한다.

기존 서비스 로직과 독립적인 개발용 스크립트이다.
CSV 데이터는 자동 다운로드하지 않는다.
"""

import argparse
import csv
import json
import re

from pathlib import Path


# ============================================================
# 1. 기본 경로 및 출처
# ============================================================

OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "localization"
    / "generated"
)

SOURCE = (
    "https://github.com/"
    "Ra-Workspace/ffxiv-datamining-ko"
)


# ============================================================
# 2. CSV에서 한국어 기술명 추출
# ============================================================

def read_action_names(
    csv_path: Path,
    id_column: str = "key",
    name_column: str = "Name",
) -> dict[str, str]:
    """
    CSV에서 Action ID → 한국어 기술명 매핑을 추출한다.

    컬럼 이름은 CSV 형식에 따라 지정할 수 있다.

    이름이 빈 행은 제외한다.
    잘못된 ID나 충돌하는 중복 데이터는 오류로 처리한다.
    """

    names: dict[str, str] = {}

    # UTF-8 BOM이 있는 CSV도 처리
    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)
        columns = reader.fieldnames or []

        # 필요한 열이 실제 CSV에 존재하는지 확인
        if (
            id_column not in columns
            or name_column not in columns
        ):
            raise ValueError(
                f"CSV 열을 찾을 수 없습니다. "
                f"실제 열: {columns}. "
                f"--id-column / --name-column을 확인하세요."
            )

        for row in reader:

            raw_id = (
                row.get(id_column) or ""
            ).strip()

            name_ko = (
                row.get(name_column) or ""
            ).strip()

            # 빈 ID 및 CSV 메타데이터 행 제외
            # '#': 필드 이름 설명 행
            # 'int32': 필드 자료형 설명 행
            if raw_id in ("", "#", "int32"):
                continue

            # Action ID는 정수 형태여야 함
            if (
                not raw_id.isascii()
                or not raw_id.isdecimal()
            ):
                raise ValueError(
                    f"CSV {reader.line_num}행의 "
                    f"Action ID가 유효하지 않습니다: {raw_id!r}"
                )

            # 이름이 없는 데이터 제외
            if not name_ko:
                continue

            # 00075 -> 75 정규화
            action_id = str(int(raw_id))

            # 같은 ID에 서로 다른 이름이 등록된 경우
            if (
                action_id in names
                and names[action_id] != name_ko
            ):
                raise ValueError(
                    f"Action ID {action_id}에 "
                    f"서로 다른 이름이 중복되었습니다: "
                    f"{names[action_id]!r}, {name_ko!r}"
                )

            names[action_id] = name_ko

    if not names:
        raise ValueError(
            "CSV에서 유효한 기술명을 찾지 못했습니다."
        )

    # Action ID 숫자 순으로 정렬
    return dict(
        sorted(
            names.items(),
            key=lambda item: int(item[0])
        )
    )


# ============================================================
# 3. JSON 데이터 구조 생성
# ============================================================

def build_mapping(
    names: dict[str, str],
    patch: str,
    source_ref: str,
) -> dict:
    """
    기존 한국어 기술명 매핑 구조에 맞는 데이터를 생성한다.

    patch: 검증된 한국 클라이언트 패치
    source_ref: CSV 원본의 Git 태그 또는 커밋 ID
    """

    if not re.fullmatch(r"\d+\.\d{1,2}", patch):
        raise ValueError(
            "패치 버전은 '7.57' 같은 형식이어야 합니다."
        )

    if not source_ref.strip():
        raise ValueError(
            "데이터 출처의 태그 또는 커밋 ID가 필요합니다."
        )

    return {
        "language": "ko",
        "patch": patch,
        "source": SOURCE,
        "source_ref": source_ref.strip(),
        "names": names,
    }


# ============================================================
# 4. JSON 파일 저장
# ============================================================

def save_mapping(
    output_path: Path,
    data: dict,
) -> None:
    """
    변환 결과를 JSON 파일로 저장한다.

    mode='x'를 사용하여 기존 파일 덮어쓰기를 방지한다.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open(
        "x",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

        file.write("\n")


# ============================================================
# 5. 명령어 인자 및 실행
# ============================================================

def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "한국어 Action CSV를 "
            "기술명 JSON으로 변환"
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="한국어 Action.csv 파일 경로"
    )

    parser.add_argument(
        "--patch",
        required=True,
        help="검증된 한국 클라이언트 패치"
    )

    parser.add_argument(
        "--source-ref",
        required=True,
        help="원본 CSV의 Git 태그 또는 커밋 ID"
    )

    parser.add_argument(
        "--id-column",
        default="key",
        help="Action ID 열 이름 (기본: key)"
    )

    parser.add_argument(
        "--name-column",
        default="Name",
        help="한국어 기술명 열 이름 (기본: Name)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="출력할 JSON 파일 경로"
    )

    args = parser.parse_args()

    output_path = (
        args.output
        or OUTPUT_DIR / f"ko_{args.patch}.json"
    )

    try:
        # CSV 읽기
        names = read_action_names(
            args.input,
            args.id_column,
            args.name_column
        )

        # JSON 데이터 구성
        payload = build_mapping(
            names,
            args.patch,
            args.source_ref
        )

        # 파일 생성
        save_mapping(output_path, payload)

    except (OSError, ValueError) as exc:
        parser.exit(
            1,
            f"변환 실패: {exc}\n"
        )

    print(f"변환 완료: {len(names)}개 Action ID")
    print(f"저장 위치: {output_path}")


if __name__ == "__main__":
    main()
