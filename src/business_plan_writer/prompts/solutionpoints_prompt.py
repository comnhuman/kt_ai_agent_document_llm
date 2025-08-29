from src.business_plan_writer.schemas import SolutionPointsInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(SolutionPointsInfo)}
이다.

[필드별 작성 가이드 & 예시]
- 주요 계획(main): "모바일 앱 서비스 프로토타입 개발(1년차 완료)", "클라우드 기반 플랫폼 고도화(2년차 진행)" 등
- 세부 계획(sub): "UI/UX 시제품 제작 후 베타 테스트 실시", "정부지원사업비는 인건비 및 장비구축에 활용, 자기부담사업비는 마케팅 비용에 배정" 등

[사업기간 내 일정(schedules) - 각 행의 예시]
- 추진 업무(task): "필수 개발 인력 채용", "제품 패키지 디자인", "홍보용 웹사이트 제작", "시제품 완성" 등
- 수행 기간(period): "00.00 ~ 00.00", "협약기간 말" 등
- 세부 설명(detail): "OO 전공 경력 직원 00명 채용", "제품 패키지 디자인 용역 진행", "웹사이트 자체 제작", "협약기간 내 시제품 제작 완료" 등


[작성 규칙]
1) 반드시 한국어로 작성.

[검색된 참고자료]
- 회사DB: None
- 공고문DB: None

위 정보를 참고하여 {list(SolutionPointsInfo.model_fields.keys())} 항목을 작성하라.'''
}