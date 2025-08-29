from src.business_plan_writer.schemas import Summary
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(Summary)}
이다.

[필드별 작성 가이드 & 예시]
- 명칭(name): "게토레이", "Windows", "알파고" 등
- 범주(category): "스포츠음료", "OS(운영체제)", "인공지능프로그램" 등
- 아이템 개요(item_overview): "OO기술이 적용된 OO제품으로, OO기능과 OO혜택 제공" 등
- 문제 인식(problem_summary): "국내 시장에서 ○○ 기술 보급률 부족, 소비자 접근성 한계" 등
- 실현 가능성(solution_summary): "사업기간 내 모바일 앱 프로토타입 개발, 기능 차별화 전략 수립" 등
- 성장 전략(scaleup_summary): "경쟁사 대비 ○○ 차별성, 글로벌 시장 진출 로드맵, 투자유치 계획" 등
- 팀 구성(team_summary): "대표자와 공동대표, 마케팅 담당자, 협력기관 ○○전자와의 협업 계획" 등


[작성 규칙]
1) 반드시 한국어로 작성.

[참고자료]
- 회사: {"{companyinfo}"}
- 공고: {"{bizinfo}"}

위 정보를 참고하여 {"{request}"}'''
}