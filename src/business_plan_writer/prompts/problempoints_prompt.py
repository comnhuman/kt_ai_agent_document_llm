from src.business_plan_writer.schemas import ProblemPointsInfo
from src.business_plan_writer.utils import build_tree

prompt = {
    "user": f'''스키마에서 이번에 채워야 할 필드는
{build_tree(ProblemPointsInfo)}
이다.

개발하고자 하는 아이템의 국내·외 시장 현황 및 문제점 등의 제시
문제 해결을 위한 아이템의 개발 필요성 등 기재_개발 아이템 소개


[작성 규칙]
1) 반드시 한국어로 작성.

[검색된 참고자료]
- 회사DB: None
- 공고문DB: None

위 정보를 참고하여 {list(ProblemPointsInfo.model_fields.keys())} 항목을 작성하라.'''
}