from src.business_plan_writer.schemas import BudgetInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(BudgetInfo)}
이다.

[필드별 작성 가이드 & 예시]
- 비목(category): "재료비", "외주용역비", "인건비" 등
- 집행 계획(plan): "DMD소켓 구입(00개x0000원)", "진입대류 구입(00개x000원)", "시급협회와 외주용역" 등
- 정부지원 사업비(gov_support): "3,448,000"
- 자기부담 사업비(self_funding): "7,000,000(현금)", "2,000,000(현물)" 등
- 총 사업비(total): "10,000,000"

[작성 규칙]
1) 반드시 한국어로 작성.

[참고자료]
- 회사: {"{companyinfo}"}
- 공고: {"{bizinfo}"}

위 정보를 참고하여 {"{request}"}'''
}