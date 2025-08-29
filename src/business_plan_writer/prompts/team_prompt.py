from src.business_plan_writer.schemas import TeamInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(TeamInfo)}
이다.

[필드별 작성 가이드 & 예시]
- 대표 및 팀원 주요 항목(team_points):
  - main: "대표자의 경력과 전문성", "팀원들의 보유 역량"
  - sub: "OO학 박사, OO과 교수 경력(00년)", "정부지원사업 수행 경험, 장비·시설 보유" 등

- 팀 구성(plan_members):
  - position: "공동대표", "대리" 등
  - task: "S/W 개발 총괄", "홍보 및 마케팅" 등
  - capability: "OO학 박사, OO 관련 경력(00년 이상)" 등
  - status: "완료(00.00)", "예정(00.00)" 등

- 협력 기관(partners):
  - name: "○○전자", "○○기업" 등
  - capability: "시제품 관련 H/W 제작·개발", "S/W 제작·개발" 등
  - plan: "테스트 장비 지원", "웹사이트 제작 용역" 등
  - period: "00.00 ~", "협약기간 내" 등


[작성 규칙]
1) 반드시 한국어로 작성.

[참고자료]
- 회사: {"{companyinfo}"}
- 공고: {"{bizinfo}"}

위 정보를 참고하여 {"{request}"}'''
}