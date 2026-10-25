
from typing import Literal

from pydantic import BaseModel, Field


# ============================================================
# 1. 기술 유형 정의
# ============================================================

# GCD: 글로벌 쿨다운이 적용되는 기술
# oGCD: 글로벌 쿨다운과 별개로 사용하는 기술
SkillType = Literal["GCD", "oGCD"]


# 자원 변화가 발생하는 조건
# on_use   : 기술 사용 시
# on_hit   : 기술 적중 시
# on_combo : 콤보 성공 시
ResourceTrigger = Literal[
    "on_use",
    "on_hit",
    "on_combo"
]


# ============================================================
# 2. 직업별 자원 변화 모델
# ============================================================

class ResourceChange(BaseModel):
    """
    기술 사용에 따른 직업 자원 변화 정보.

    예시:
        amount = 40  → 자원 40 획득
        amount = -50 → 자원 50 소비

    이 모델은 변화량만 정의한다.
    실제 자원 계산은 시뮬레이션 엔진에서 처리한다.
    """

    # 자원 식별자
    resource_key: str = Field(min_length=1)

    # 양수: 획득 / 음수: 소비
    amount: int

    # 자원 변화가 발생하는 조건
    trigger: ResourceTrigger = "on_use"


# ============================================================
# 3. 버프 효과 모델
# ============================================================

class BuffEffect(BaseModel):
    """
    개인 버프 및 파티 시너지 효과.

    crit_rate_bonus = 0.10
        → 극대화 확률 10%p 증가

    damage_multiplier = 1.05
        → 피해량 5% 증가
    """

    # 버프 지속시간 (초)
    duration_seconds: float = Field(gt=0)

    # 버프 적용 대상
    target: Literal["self", "party"] = "self"

    # 극대화 확률 증가량
    crit_rate_bonus: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    # 직격 확률 증가량
    direct_hit_rate_bonus: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    # 피해량 배율
    damage_multiplier: float = Field(
        default=1.0,
        gt=0.0
    )


# ============================================================
# 4. 기술 공통 모델
# ============================================================

class Skill(BaseModel):
    """
    모든 직업에서 사용하는 공통 기술 데이터 모델.

    직업별 기술은 동일한 구조로 저장하며,
    실제 기술 효과 및 발동 조건은 추후 확장한다.
    """

    # -------------------------
    # 기술 기본 정보
    # -------------------------
    id: str = Field(min_length=1)

    # XIVAPI 영어 기술명
    name: str = Field(min_length=1)

    # 공식 한국어 기술명
    name_ko: str | None = None

    gcd_type: SkillType
    required_level: int = Field(ge=1)

    # -------------------------
    # 기술 위력
    # -------------------------

    # 기본 위력
    # 공격하지 않는 버프 기술은 0
    potency: int = Field(default=0, ge=0)

    # 콤보 성공 시 적용되는 위력
    combo_potency: int | None = Field(
        default=None,
        ge=0
    )

    # 선행 콤보 기술 ID
    combo_from: str | None = None

    # -------------------------
    # 재사용 시간
    # -------------------------

    # 기본 재사용 시간 (초)
    base_recast_seconds: float | None = Field(
        default=None,
        gt=0
    )

    # 별도 쿨타임 (초)
    cooldown_seconds: float | None = Field(
        default=None,
        ge=0
    )

    # 기술 최대 충전 횟수
    max_charges: int = Field(
        default=1,
        ge=1
    )

    # 애니메이션 락 시간
    animation_lock_seconds: float | None = Field(
        default=None,
        ge=0
    )

    # -------------------------
    # 기술 아이콘
    # -------------------------

    icon_url: str | None = None

    # -------------------------
    # 직업 자원 시스템
    # -------------------------

    # 기술 사용에 필요한 최소 자원량
    resource_requirements: dict[str, int] = Field(
        default_factory=dict
    )

    # 기술 사용으로 발생하는 자원 증감
    resource_changes: list[ResourceChange] = Field(
        default_factory=list
    )

    # -------------------------
    # 버프 효과
    # -------------------------

    # 버프가 없는 기술은 None
    buff: BuffEffect | None = None


# ============================================================
# 5. 직업별 기술 데이터셋
# ============================================================

class SkillDataset(BaseModel):
    """
    직업 / 레벨 / 패치별 기술 데이터 묶음.

    예시:
        job = "DRG"
        level = 100
        patch = "7.10"
        source = "xivapi"
    """

    # 직업 코드
    job: str = Field(min_length=1)

    # 레벨
    level: int = Field(ge=1)

    # 패치 버전 (예: "7.05", "7.10")
    # 버전 표기를 보존하기 위해 str 사용
    patch: str = Field(min_length=1)

    # 기술 데이터 출처
    source: str = Field(
        default="prototype",
        min_length=1
    )

    # 해당 직업의 기술 목록
    skills: list[Skill] = Field(
        default_factory=list
    )
