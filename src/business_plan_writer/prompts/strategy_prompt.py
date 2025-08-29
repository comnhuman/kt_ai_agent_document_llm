from src.business_plan_writer.schemas import StrategyInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(StrategyInfo)}
이다.

[필드별 작성 가이드 & 예시]
- 주요 전략(main): "제품 성능 고도화", "해외 시장 진출", "지속적 업데이트를 통한 경쟁력 유지" 등
- 세부 전략(sub): "국내외 특허 확보", "품질 인증 취득", "해외 파트너사 협력 체계 구축" 등

[사업화·확산 일정(scaleup_schedules) - 각 행의 예시]
- 추진 업무(task): "필수 개발 인력 채용", "제품 패키지 디자인", "홍보용 웹사이트 제작", "시제품 완성" 등
- 수행 기간(period): "00.00 ~ 00.00", "협약기간 말" 등
- 세부 설명(detail): "OO 전공 경력 직원 00명 채용", "제품 패키지 디자인 용역 진행", "웹사이트 자체 제작", "협약기간 내 시제품 제작 완료" 등


[작성 규칙]
1) 반드시 한국어로 작성.

[검색된 참고자료]
- 회사DB: None
- 공고문DB: None

위 정보를 참고하여 {list(StrategyInfo.model_fields.keys())} 항목을 작성하라.'''
}