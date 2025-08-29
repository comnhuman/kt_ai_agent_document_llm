from pydantic import BaseModel, Field
from typing import Union

class GeneralMember(BaseModel):
    """팀 구성 현황(대표자 본인 제외)의 한 행"""
    position: str = Field(default="", description="직위")
    task: str = Field(default="", description="담당 업무")
    capability: str = Field(default="", description="보유 역량")
    status: str = Field(default="", description="구성 상태")

class GeneralInfo(BaseModel):
    """사업계획서 - 일반현황 섹션"""
    item_name: str = Field(default="", description="사업아이템명")
    deliverables: str = Field(default="", description="산출물(협약기간 내 목표)")
    job: str = Field(default="", description="직업(직장명 기재 불가)")
    company_name: str = Field(default="", description="기업(예정)명")
    general_members: list[GeneralMember] = Field(
        default_factory=list,
        description="팀 구성 현황 리스트(대표자 본인 제외)"
    )

class ProblemPoint(BaseModel):
    """국내·외 시장 현황 및 문제점 등"""
    main: str = Field(
        default="",
        description="주요 문제점 (시장 현황, 기술적/산업적 한계 등)"
    )
    sub: str = Field(
        default="",
        description="세부 문제점 또는 설명"
    )

class ProblemPointsInfo(BaseModel):
    """사업계획서 - 개발 아이템 소개 및 문제점 섹션"""
    problem_points: list[ProblemPoint] = Field(
        default_factory=list,
        description=(
            "개발하고자 하는 아이템의 국내·외 시장 현황 및 문제점 제시, "
            "이를 해결하기 위한 아이템 개발 필요성 기재"
        )
    )

class SolutionPoint(BaseModel):
    """아이디어를 제품·서비스로 개발 및 구체화하는 계획"""
    main: str = Field(
        default="",
        description="주요 계획 (예: 프로토타입 개발, 플랫폼 고도화 등)"
    )
    sub: str = Field(
        default="",
        description=(
            "세부 계획 (예: 일정, 기능·성능 차별성, 경쟁력 확보 전략, "
            "정부지원사업비 및 자기부담사업비 집행 계획 등)"
        )
    )

class Schedule(BaseModel):
    """사업기간 내 일정 세부 계획"""
    task: str = Field(
        default="",
        description="추진 내용"
    )
    period: str = Field(
        default="",
        description="추진 기간"
    )
    detail: str = Field(
        default="",
        description="세부 내용"
    )

class SolutionPointsInfo(BaseModel):
    """사업계획서 - 개발 계획 및 경쟁력 전략 섹션"""
    solution_points: list[SolutionPoint] = Field(
        default_factory=list,
        description=(
            "아이디어를 제품·서비스로 개발 또는 구체화하는 일정 및 계획, "
            "개발 아이템의 차별성과 경쟁력 확보 전략, "
            "정부지원사업비 및 자기부담사업비 집행 계획을 포함"
        )
    )
    schedules: list[Schedule] = Field(
        default_factory=list,
        description="사업기간 내 일정별 세부 계획"
    )

class Budget(BaseModel):
    """사업비 집행 계획의 한 행"""
    category: str = Field(
        default="",
        description="비목"
    )
    plan: str = Field(
        default="",
        description="집행 계획"
    )
    gov_support: str = Field(
        default="",
        description="정부지원 사업비 금액"
    )
    self_funding: str = Field(
        default="",
        description="자기부담 사업비 금액"
    )
    total: str = Field(
        default="",
        description="총 사업비 금액"
    )

class BudgetInfo(BaseModel):
    """사업계획서 - 사업비 집행 계획 섹션"""
    budgets: list[Budget] = Field(
        default_factory=list,
        description="사업비 집행 계획 리스트"
    )

class Strategy(BaseModel):
    """아이템의 기능·성능 차별성 및 경쟁력 확보 전략"""
    main: str = Field(
        default="",
        description="주요 전략"
    )
    sub: str = Field(
        default="",
        description="세부 전략 또는 실행 방법"
    )

class ScaleupSchedule(BaseModel):
    """아이템 사업화·확산(Scale-up) 일정"""
    task: str = Field(
        default="",
        description="주요 업무 또는 활동"
    )
    period: str = Field(
        default="",
        description="수행 기간"
    )
    detail: str = Field(
        default="",
        description="세부 설명"
    )

class StrategyInfo(BaseModel):
    """사업계획서 - 실현 가능성 및 Scale-up 전략 섹션"""
    strategies: list[Strategy] = Field(
        default_factory=list,
        description="아이템의 기능·성능 차별성 및 경쟁력 확보 전략 리스트"
    )
    scaleup_schedules: list[ScaleupSchedule] = Field(
        default_factory=list,
        description="아이템 사업화·확산(Scale-up) 추진 일정"
    )

class TeamPoint(BaseModel):
    """대표자 및 팀원 구성 계획의 주요 항목"""
    main: str = Field(
        default="",
        description="주요 항목"
    )
    sub: str = Field(
        default="",
        description="세부 설명"
    )

class PlanMember(BaseModel):
    """팀 구성(대표자 제외)"""
    position: str = Field(
        default="",
        description="직위"
    )
    task: str = Field(
        default="",
        description="담당 업무"
    )
    capability: str = Field(
        default="",
        description="보유 역량"
    )
    status: str = Field(
        default="",
        description="구성 상태"
    )

class Partner(BaseModel):
    """협력 기관 현황 및 협업 방안"""
    name: str = Field(
        default="",
        description="협력 기관명"
    )
    capability: str = Field(
        default="",
        description="기관이 보유한 역량"
    )
    plan: str = Field(
        default="",
        description="협업 방안"
    )
    period: str = Field(
        default="",
        description="협력 시기"
    )

class TeamInfo(BaseModel):
    """사업계획서 - 팀 구성 및 협력 기관 섹션"""
    team_points: list[TeamPoint] = Field(
        default_factory=list,
        description="대표자 및 팀원 구성 계획의 주요 항목 리스트"
    )
    plan_members: list[PlanMember] = Field(
        default_factory=list,
        description="팀 구성(대표자 제외)"
    )
    partners: list[Partner] = Field(
        default_factory=list,
        description="협력 기관 현황 및 협업 방안 리스트"
    )

class Summary(BaseModel):
    """아이템 개요(요약)"""
    name: str = Field(
        default="",
        description="아이템 명칭"
    )
    category: str = Field(
        default="",
        description="아이템 범주"
    )
    item_overview: str = Field(
        default="",
        description="아이템 개요: 제품·서비스의 사용 용도, 사용 가격, 핵심 기능·성능, 고객 제공 혜택 등"
    )
    problem_summary: str = Field(
        default="",
        description="문제 인식: 국내·외 시장 현황 및 문제점, 이를 해결하기 위한 창업 아이템 필요성"
    )
    solution_summary: str = Field(
        default="",
        description="실현 가능성: 사업기간 내 개발 계획, 차별성 및 경쟁력 확보 전략"
    )
    scaleup_summary: str = Field(
        default="",
        description="성장 전략: 경쟁사 분석, 시장 진입 전략, 사업 모델, 로드맵 및 투자유치 전략"
    )
    team_summary: str = Field(
        default="",
        description="팀 구성: 대표자, 팀원, 협력 파트너 등 역할과 활용 계획"
    )