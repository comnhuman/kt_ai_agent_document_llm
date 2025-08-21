# 🚀 지원사업 데이터 수집 & 사업계획서 초안 작성 Agent

> 중소기업 지원사업 정보를 기업마당 API를 통해 수집하고, vLLM을 사용하여 사용자 맞춤형 지원사업을 추천하고 사업계획서 작성하는 Agent 입니다.

---

## 📖 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [vLLM Matching System](#-vllm-matching-system)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## 📌 About
이 프로젝트는 [기업마당](https://www.bizinfo.go.kr)에서 제공하는 중소기업 지원사업 정보 API를 활용하여 데이터를 수집하고, **vLLM을 사용하여 사용자의 사업분야와 사업내용에 맞는 맞춤형 지원사업을 추천**하는 AI 시스템입니다.

### 주요 기능
- 기업마당 API를 통한 지원사업 정보 수집
- vLLM을 활용한 지능형 지원사업 매칭
- 사용자 사업분야 분석 및 맞춤형 추천
- 수집된 데이터를 JSON 형태로 저장
- 상세한 로깅을 통한 모니터링

### 기대 효과
- 중소기업 지원사업 정보의 체계적 수집
- AI 기반 맞춤형 지원사업 추천
- 데이터 분석 및 연구를 위한 기반 제공
- 자동화된 정보 수집으로 시간 절약

---

## ✨ Features
- 🔍 **다양한 검색 옵션**: 분야별, 해시태그별, 페이지네이션 지원
- 🤖 **vLLM 매칭 시스템**: 사용자 정보 기반 지능형 지원사업 추천
- 📊 **JSON 데이터 저장**: 수집된 데이터를 구조화된 JSON 형태로 저장
- 📝 **상세한 로깅**: API 요청/응답 과정을 상세히 기록
- 🛡️ **에러 처리**: 네트워크 오류, API 오류 등에 대한 안전한 처리
- 🔧 **확장 가능한 구조**: 새로운 기능 추가가 용이한 모듈화된 구조

---

## 🛠 Tech Stack
**Backend**: Python 3.8+  
**HTTP Client**: requests  
**AI/ML**: vLLM  
**Data Format**: JSON  
**Logging**: Python logging module  

---

## ⚡ Getting Started

### Prerequisites
- Python >= 3.8
- 기업마당 API 키 (발급 문의: 02-867-9765)
- GPU (vLLM 사용을 권장)

### Installation
```bash
# 1. Clone repository
git clone https://github.com/username/kt_ai_agent_document_llm.git

# 2. Move to project directory
cd kt_ai_agent_document_llm

# 3. Install dependencies
pip install -r requirements.txt

# 4. API 키 설정
# .env 파일 생성 후 BIZINFO_API_KEY 설정
echo "BIZINFO_API_KEY=your_api_key_here" > .env
```

### Quick Start
```bash
# 기본 API 데이터 수집
python src/parsing.py

# vLLM 매칭 시스템 테스트
python src/test_vllm_matcher.py

# 전체 파이프라인 실행
python src/vllm_matcher.py
```

---

## 📚 API Documentation

### 기업마당 API 정보
- **URL**: https://www.bizinfo.go.kr/uss/rss/bizinfoApi.do
- **방식**: GET
- **데이터 형식**: JSON, XML(RSS)
- **인증**: API 키 필요

### 주요 파라미터
| 파라미터명 | 타입 | 필수여부 | 설명 |
|-----------|------|----------|------|
| crtfcKey | String | Y | 서비스 인증키 |
| dataType | String | N | 데이터 타입 (rss/json) |
| searchCnt | String | N | 조회건수 |
| searchLclasId | String | N | 분야 코드 |
| hashtags | String | N | 해시태그 |
| pageUnit | String | N | 페이지당 데이터 개수 |
| pageIndex | String | N | 페이지 번호 |

### 분야 코드
- 01: 금융
- 02: 기술
- 03: 인력
- 04: 수출
- 05: 내수
- 06: 창업
- 07: 경영
- 09: 기타

---

## 🤖 vLLM Matching System

### 시스템 구조
1. **데이터 추출**: `all_categories.json`에서 `pblancNm`과 `bsnsSumryCn` 추출
2. **사용자 분석**: 사용자의 `category`와 `main_business_summary` 분석
3. **vLLM 매칭**: AI 모델을 사용한 지능형 지원사업 매칭
4. **결과 생성**: 매칭된 지원사업을 원본 데이터와 함께 저장

### 매칭 프로세스
```python
from src.vllm_matcher import VLLMMatcher
from src.user import User

# 사용자 정보 생성
user = User(
    name="테스트 사용자",
    code="02",
    main_category=["기술", "경영"],
    main_business_summary="AI 기반 개인정보 관리 컨설팅"
)

# vLLM 매처 초기화
matcher = VLLMMatcher()

# 지원사업 매칭
extracted_data = matcher.extract_support_programs_info("src/all_categories.json")
matched_programs = matcher.match_support_programs(user, extracted_data)

# 결과 저장
matcher.create_matched_output_file(matched_programs, "src/all_categories.json", "output.json")
```

---

## 💡 Usage Examples

### 기본 API 사용법
```python
from src.parsing import BizInfoAPI

# API 클라이언트 생성
api_client = BizInfoAPI()

# 기본 조회
data = api_client.get_support_programs(
    data_type="json",
    search_cnt=100
)

# JSON 파일로 저장
api_client.save_to_json(data, "support_programs.json")
```

### vLLM 매칭 사용법
```python
from src.vllm_matcher import VLLMMatcher
from src.user import User

# 사용자 정보
user = User(
    name="AI 스타트업",
    code="02",
    main_category=["기술"],
    main_business_summary="AI 기반 솔루션 개발"
)

# vLLM 매칭
matcher = VLLMMatcher()
extracted_data = matcher.extract_support_programs_info("src/all_categories.json")
matched_programs = matcher.match_support_programs(user, extracted_data)

print(f"매칭된 지원사업 수: {len(matched_programs)}")
```

---

## 📁 Project Structure
```
kt_ai_agent_document_llm/
├── main.py                    # 메인 실행 파일
├── requirements.txt           # Python 의존성
├── README.md                 # 프로젝트 문서
├── src/                      # 소스 코드 디렉토리
│   ├── parsing.py            # 기업마당 API 클라이언트
│   ├── vllm_matcher.py       # vLLM 매칭 시스템 (핵심)
│   ├── test_vllm_matcher.py  # vLLM 매처 테스트
│   ├── config.py             # 설정 관리
│   ├── user.py               # 사용자 정보 클래스
│   ├── user_catergory_mapping.py  # 사용자-카테고리 매핑
│   ├── all_categories.json   # 수집된 전체 데이터
│   └── *.json               # 기타 수집된 데이터 파일들
├── user/                     # 사용자 관련 디렉토리
└── venv/                     # Python 가상환경
```

---

## 📄 License
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 📞 Support
- **API 키 발급 문의**: 02-867-9765
- **기업마당 홈페이지**: https://www.bizinfo.go.kr
- **API 상세 문서**: https://www.bizinfo.go.kr/web/lay1/program/S1T175C174/apiDetail.do?id=bizinfoApi
