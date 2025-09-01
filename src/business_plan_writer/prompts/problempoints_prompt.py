from src.business_plan_writer.schemas import ProblemPointsInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(ProblemPointsInfo)}
이다.

[작성 지침]
- 개발하고자 하는 아이템의 국내·외 시장 현황 및 문제점을 구체적으로 제시하라.
- 문제 해결을 위한 아이템의 개발 필요성을 반드시 포함하라.
- 주요 문제(main)는 최소 3개 이상 작성하라.

[작성 규칙]
1) 반드시 한국어로 작성.

[참고자료]
- 회사: {"{companyinfo}"}
- 공고: {"{bizinfo}"}

위 정보를 참고하여 {"{request}"}'''
}