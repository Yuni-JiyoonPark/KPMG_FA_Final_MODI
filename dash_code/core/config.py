# 파일명: all3/core/config.py

import os
from dotenv import load_dotenv
import logging

# 로깅 설정 (다른 곳에서 이미 설정했다면 중복될 수 있으니 확인 필요)
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- .env 파일 로드 ---
# app.py를 실행하는 위치(보통 프로젝트 루트)나 상위 폴더에서 .env를 찾습니다.
dotenv_loaded = load_dotenv()
if dotenv_loaded:
    logger.info(".env 파일 로드 성공")
else:
    logger.warning(".env 파일을 찾지 못했습니다. 환경 변수를 직접 설정해야 할 수 있습니다.")
# ---------------------

# --- 기존 all3 설정 ---
# MySQL 데이터베이스 설정 - 매거진
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'your_db_host_name'),
    'user': os.getenv('DB_USER', 'your_db_user_name'),
    'password': os.getenv('DB_PASSWORD', ''), # .env 에 DB_PASSWORD=your_password 추가 권장
    'database': os.getenv('DB_NAME', 'your_db_name'),
    'port': int(os.getenv('DB_PORT', 'your_db_port'))
}
# MySQL 데이터베이스 설정 - 뉴스
NEWS_DB_CONFIG = {
    'host': os.getenv('NEWS_DB_HOST', 'your_db_host_name'),
    'user': os.getenv('NEWS_DB_USER', 'your_db_user_name'),
    'password': os.getenv('NEWS_DB_PASSWORD', ''), # .env 에 NEWS_DB_PASSWORD=your_password 추가 권장
    'database': os.getenv('NEWS_DB_NAME', 'your_db_name'),
    'port': int(os.getenv('NEWS_DB_PORT', 'your_db_port'))
}
# 기존 DB 설정 (호환성 유지)
DB_CONFIG = MYSQL_CONFIG
# 앱 설정
APP_CONFIG = {
    'debug': os.getenv('APP_DEBUG', 'False').lower() == 'true',
    # SECRET_KEY도 .env 에서 읽어오는 것이 좋습니다.
    'secret_key': os.getenv('SECRET_KEY', 'a-very-secret-random-key-change-me'), # 실제 키로 변경 권장
    'static_folder': os.getenv('STATIC_FOLDER', 'static'),
    'template_folder': os.getenv('TEMPLATE_FOLDER', 'templates')
}
# 기본 설정값
DEFAULT_PERIOD = os.getenv('DEFAULT_PERIOD', '7일')
DEFAULT_MAGAZINE = os.getenv('DEFAULT_MAGAZINE', 'W')
DEFAULT_KEYWORD = os.getenv('DEFAULT_KEYWORD', 'Y2K')
MAGAZINE_CHOICES = os.getenv('MAGAZINE_CHOICES', 'Vogue,W,Harper\'s').split(',')
# 기간별 일수 매핑
PERIOD_DAYS = {
    '7일': 7,
    '2주': 14,
    '1개월': 30,
    '3개월': 90,
    '6개월': 180,
    '1년': 365,
    '1주일': 7
}
# 카테고리 키워드, 불용어, 시각화 설정 등 기존 설정 유지
CATEGORY_KEYWORDS = {
    '의류': ['드레스', '재킷', '팬츠', '스커트', '코트', '블라우스', '캐주얼상의', '점프수트', '니트웨어', '셔츠', '탑', '청바지', '수영복', '점퍼', '베스트', '패딩'],
    '신발': ['구두', '샌들', '부츠', '스니커즈', '로퍼', '플립플롭', '슬리퍼', '펌프스'],
    '액세서리': ['목걸이', '귀걸이', '반지', '브레이슬릿', '시계', '선글라스', '스카프', '벨트', '가방'],
    '가방': ['백팩', '토트백', '크로스백', '클러치', '숄더백', '에코백'],
    '기타': ['화장품', '향수', '주얼리', '선글라스', '시계']
}
STOPWORDS = set([
    '것', '수', '등', '더', '위해', '또한', '있는', '하는', '에서', '으로',
    '그리고', '이번', '한편', '있다', '했다', '대한', '가장', '이런',
    '한다', '한다면', '바', '때', '다양한', '통해', '기자', '최근',
    '우리', '많은', '중', '때문', '대한', '모든', '하지만', '중인',
    '이후', '그녀', '그는', '에서의', '있는지', '중심', '된다', '있으며',
    '된다', '된다면', '위한','스타일링', '스타일', '아이템', '패션', '브랜드',
    '컬렉션', '코디', '컬러', '트렌드', '디자이너', '쇼핑', '코디', '코디네이터', '코디법', '코디추천', '코디아이템', '박소현', '황기애', '정혜미', '진정',
    '무드', '느낌', '분위기', '매력', '활용', '완성', '연출', '선택', '조합', '포인트', '다양', '모습', '자신', '사람', '마음',
    '제품', '디자인', '에디터', '정윤', '보그', '년대', '등장' '시즌', '스타일링', '스타일', '아이템', '패션', '브랜드', '장진영', '윤다희', '강미', '박은아',
])
VISUALIZATION_CONFIG = {
    'network_graph': {'node_size': 600, 'edge_width': 2, 'font_size': 10},
    'wordcloud': {'width': 800, 'height': 400, 'max_words': 100},
    'category_chart': {'figsize': (10, 6), 'colors': ['#36D6BE', '#6B5AED', '#FF5A5A', '#4A78E1', '#FFA26B']},
    'trend_chart': {'figsize': (12, 6), 'marker_size': 8, 'line_width': 2}
}
DEFAULT_LIMIT = 1000
MAX_KEYWORDS = 20
# --- 기존 설정 끝 ---


# --- '검색기' RAG 시스템 관련 설정 추가 및 수정 ---

# LLM API 설정
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_URL = os.getenv('LLM_API_URL', 'your_api_url')

# API 키 로드 확인 및 경고
if not LLM_API_KEY:
    logger.warning("!!! 경고: LLM_API_KEY 환경변수 또는 .env 파일에서 OpenAI API 키를 찾을 수 없습니다. RAG 기능이 작동하지 않을 수 있습니다 !!!")
else:
    logger.info("LLM_API_KEY 로드됨 (값은 보안상 출력하지 않음)")


# --- RAG 데이터 경로 설정 (사용자가 알려준 경로 기준) ---
# 환경 변수 'RAG_DATA_BASE_PATH'가 있으면 사용하고, 없으면 제공된 절대 경로를 기본값으로 사용
RAG_DATA_BASE_PATH = os.getenv('RAG_DATA_BASE_PATH', '/your_path/검색기/datas')
logger.info(f"RAG 데이터 기본 경로 설정: {RAG_DATA_BASE_PATH}")
# !!! 중요: 위 경로는 '/Users/pjh_air/' 환경에만 해당됩니다. 다른 환경에서는 환경 변수를 사용하거나 경로를 수정해야 합니다. !!!

# 하위 디렉토리 경로 정의 (os.path.join 사용)
RAG_DOCS_DIR = os.path.join(RAG_DATA_BASE_PATH, 'docs')
RAG_VECS_DIR = os.path.join(RAG_DATA_BASE_PATH, 'vecs')
RAG_BACKUP_DIR = os.path.join(RAG_DATA_BASE_PATH, 'backup')  # 필요시 사용

# --- RAG 파일 경로 설정 (os.path.join 사용 및 파일명 확인) ---
# *** 중요: 아래 파일명들이 실제 위의 'datas/docs' 와 'datas/vecs' 폴더 안에 있는지 확인하세요! ***

# 문서 파일 경로 ('검색기/config.py' 내용 반영)
FASHION_DOC_PATH = os.getenv('FASHION_DOC_PATH', os.path.join(RAG_DOCS_DIR, 'fashion_document_raw.json'))
MUSINSA_DOC_PATH = os.getenv('MUSINSA_DOC_PATH', os.path.join(RAG_DOCS_DIR, 'musinsa_raw.json'))
# RAG 시스템이 벡터 포함 파일(_vecs.json)을 사용한다면 파일명을 변경해야 합니다.
# FASHION_DOC_PATH = os.getenv('FASHION_DOC_PATH', os.path.join(RAG_DOCS_DIR, 'fashion_document_raw_vecs.json'))
# MUSINSA_DOC_PATH = os.getenv('MUSINSA_DOC_PATH', os.path.join(RAG_DOCS_DIR, 'musinsa_raw_vecs.json'))


# 벡터 파일 경로 (실제 파일명으로 수정 필수!)
# *** 중요: '/Users/pjh_air/Documents/0409_정훈 복사본/검색기/datas/vecs/' 안에 있는 실제 벡터 파일 이름으로 바꾸세요! ***
DOC_VECS_PATH = os.getenv('DOC_VECS_PATH', os.path.join(RAG_VECS_DIR, 'doc_vec.json'))  # 예: 'doc_vec_20250405_115708.json' 등
ENT_VECS_PATH = os.getenv('ENT_VECS_PATH', os.path.join(RAG_VECS_DIR, 'ent_vec.json'))  # 예: 'ent_vec_20250405_115708.json' 등

# 핫 키워드 파일 저장 디렉토리
HOT_KEYWORDS_DIR = os.getenv('HOT_KEYWORDS_DIR', RAG_DOCS_DIR)  # 문서 디렉토리와 동일하게 설정

# 경로 설정 로그 출력
logger.info(f"Fashion Doc Path 설정: {FASHION_DOC_PATH}")
logger.info(f"Musinsa Doc Path 설정: {MUSINSA_DOC_PATH}")
logger.info(f"Document Vector Path 설정: {DOC_VECS_PATH}")
logger.info(f"Entity Vector Path 설정: {ENT_VECS_PATH}")
logger.info(f"Hot Keywords Directory 설정: {HOT_KEYWORDS_DIR}")

# --- RAG 분석 설정 (기존 '검색기/config.py' 내용 반영) ---
HOT_KEYWORDS_MIN_LENGTH = int(os.getenv('HOT_KEYWORDS_MIN_LENGTH', 4))
DEFAULT_TOP_K = int(os.getenv('DEFAULT_TOP_K', 5))
HOT_KEYWORDS_MAX_COUNT = int(os.getenv('HOT_KEYWORDS_MAX_COUNT', 10))

# --- 설정 추가 끝 ---

# --- 경로 존재 여부 확인 함수 (디버깅용) ---
def check_paths():
    paths_to_check = {
        "RAG 데이터 기본 경로": RAG_DATA_BASE_PATH,
        "RAG 문서 디렉토리": RAG_DOCS_DIR,
        "RAG 벡터 디렉토리": RAG_VECS_DIR,
        "패션 문서 파일": FASHION_DOC_PATH,
        "무신사 문서 파일": MUSINSA_DOC_PATH,
        "문서 벡터 파일": DOC_VECS_PATH,
        "엔티티 벡터 파일": ENT_VECS_PATH,
        "핫 키워드 저장 디렉토리": HOT_KEYWORDS_DIR
    }
    all_paths_ok = True
    logger.info("--- 경로 설정 확인 시작 ---")
    for name, path in paths_to_check.items():
        exists = os.path.exists(path)
        is_dir = os.path.isdir(path) if exists else False
        is_file = os.path.isfile(path) if exists else False
        status = "OK" if exists else "ERROR: Not Found!"
        type_info = " (디렉토리)" if is_dir else (" (파일)" if is_file else "")
        logger.info(f"{name}: {path} [{status}{type_info}]")
        if not exists:
             all_paths_ok = False
    if not all_paths_ok:
         logger.warning("!!! 일부 RAG 데이터 경로/파일을 찾을 수 없습니다. 위의 로그 및 경로 설정을 확인하세요. !!!")
    logger.info("--- 경로 설정 확인 끝 ---")

# 앱 시작 시 경로 확인 로그 출력
check_paths()
# --- 경로 확인 끝 ---