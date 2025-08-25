from pathlib import Path
from openai import OpenAI
from typing import Union
from src.user import User
from dotenv import load_dotenv
import os
import base64
import logging

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_env_var(var_name: str):
    """환경변수를 확인하고 없으면 사용자 입력을 받아 등록"""
    value = os.environ.get(var_name)
    if not value:
        logger.warning(f"[환경변수 {var_name}]가 등록되어 있지 않습니다.")
        value = input(f"{var_name} 값을 입력하세요: ").strip()
        os.environ[var_name] = value
        logger.info(f"[환경변수 {var_name}]가 새로 등록되었습니다.")
    else:
        logger.info(f"[환경변수 {var_name}] 등록되어 있음.")
    return os.environ[var_name]

def write_application(
    user: User,
    pdf_path: Union[str, Path],
):
    with open(pdf_path, "rb") as f:
        data = f.read()
    base64_string = base64.b64encode(data).decode("utf-8")

    ensure_env_var("OPENAI_API_KEY")
    client = OpenAI()
    logger.info("OpenAI API GPT-5 답변 생성 중...")
    response = client.responses.create(
        model="gpt-5",
        # previous_response_id=response.id,
        input=[
            {
                "role": "developer",
                "content": f'''
## 1. 입력 데이터

* **사용자 정보**

{user}
* **문서 파일**

  * 사업 공고에 첨부된 양식, 서식, 신청서 (주로 PDF)

---

## 2. 수행 목적

* 입력된 PDF 문서의 **필수 항목 및 작성 칸**을 분석한다.
* 사용자 정보를 토대로 자동으로 **초안 문서를 생성**한다.
* 공란이나 선택 항목은 문맥을 분석해 합리적 기본값 또는 placeholder를 채운다.
* 최종 결과는 **사업 공고 제출용 맞춤 문서**로 제공한다.

---

## 3. 동작 절차

### 3.1 PDF 분석

1. 문서 구조를 파악한다 (제목, 섹션, 표, 입력칸, 필수 작성란).
2. 입력란(Label)과 항목별 요구사항(예: “신청인 성명”, “사업자 등록번호”, “주요 사업내용”)을 추출한다.

### 3.2 사용자 정보 매핑

* PDF의 항목과 `User` 객체 속성을 자동 매핑한다.

  * `name` → 신청인 성명, 대표자명
  * `code` → 신청 코드, 식별 번호, 내부 분류 등
  * `main_category` → 주요 업종, 사업 분야
  * `main_business_summary` → 사업 개요, 회사 소개, 주요 기술 설명

### 3.3 추가 항목 처리

* 사용자 정보에 없는 항목은 **빈칸** 또는 `[추가 입력 필요]`로 표시.
* 공고 특성상 자주 요구되는 항목(예: 주소, 연락처, 매출액, 인원 수 등)은 **placeholder**로 채운다.

  * 예: "연락처: [전화번호 입력]"
  * 예: "주소: [사업장 주소 입력]"

### 3.4 문서 작성

1. 추출된 입력칸에 사용자 정보를 채워 Word 형식의 결과물을 생성한다.
2. 문서 전체를 **가독성 있는 문장**으로 보완하며, 사업 공고에 어울리는 문체(격식, 공식 문서 스타일)로 작성한다.
3. 필요시 **요약/확장**:

   * 사업 개요는 1~2문단으로 정리.
   * 주요 카테고리는 목록 형식으로 정리.

---

## 4. 출력 결과

* **완성된 문서(초안)**: 사업 공고 제출용 Word 형식
* **자동 채움 보고서**:

  * 매핑된 사용자 정보 항목
  * Placeholder가 삽입된 항목 리스트
  * 추가 입력이 필요한 부분 안내
'''
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": "draconomicon.pdf",
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                    # {
                    #     "type": "input_text",
                    #     "text": "무엇이 적혀있지?",
                    # },
                ],
            },
        ],
        store=True
    )

    logger.info(response.output_text)

    return response.output_text

if __name__ == "__main__":
    user = User(
        "test",
        "02",
        ["기술", "경영"],
        "제 사업은 개인정보 관리실태 컨설팅입니다. 현재 AI 를 활용한 자동화 사업에 도전하고 있습니다."
        )

    import requests
    import tempfile
    dummy_pdf = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    response = requests.get(dummy_pdf)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(response.content)
    tmp.close()

    write_application(user, tmp.name)