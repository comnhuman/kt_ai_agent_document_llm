from src.business_plan_writer.schemas import GeneralInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(GeneralInfo)}
이다.

[필드별 작성 가이드 & 예시]
- 사업아이템명: "OO기술이 적용된 OO기능의(혜택을 제공하는) OO제품·서비스 등"
- 산출물(협약기간 내 목표): "모바일 어플리케이션(0개), 웹사이트(0개)"
- 직업(직장명 기재 불가): "교수 / 연구원 / 사무직 / 일반인 / 대학생 등"
- 기업(예정)명

[팀 구성 현황 리스트(대표자 본인 제외) - 각 행의 예시]
- 직위: "공동대표", "대리" 등
- 담당 업무: "S/W 개발 총괄", "홍보 및 마케팅" 등
- 보유 역량: "OO학 학사", "OO 관련 경력(00년 이상)"
- 구성 상태: "완료", "예정"

[작성 규칙]
1) 반드시 한국어로 작성.

[검색된 참고자료]
- 회사DB: None
- 공고문DB: None


위 정보를 참고하여 {list(GeneralInfo.model_fields.keys())} 항목을 작성하라.'''
}
