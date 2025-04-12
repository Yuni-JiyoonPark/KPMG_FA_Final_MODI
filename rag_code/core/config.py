# config.py

# OpenAI API 설정
LLM_API_KEY = # 실제 키로 교체 필요
LLM_API_URL =  # OpenAI API 엔드포인트



# 경로 설정 - 실제 파일 경로로 수정
DATA_DIR = 
DOCS_DIR = 
BACKUP_DIR = 
VECS_DIR = 

# 파일 경로 설정
FASHION_DOC_PATH = 
MUSINSA_DOC_PATH = 
DOC_VECS_PATH = 
ENT_VECS_PATH = 

# 시간 주기 정의
PERIOD_DAYS = {
    "전체": None,  # None = 전체 기간
    "1주일": 7,
    "1개월": 30,
    "3개월": 90,
    "6개월": 180,
    "1년": 365
}

# 트렌드 분석 설정
HOT_KEYWORDS_MIN_LENGTH = 4  # 핫 키워드 최소 길이
DEFAULT_TOP_K = 5  # 기본 검색 결과 수
HOT_KEYWORDS_MAX_COUNT = 10  # 레포트에 포함할 최대 핫 키워드 수