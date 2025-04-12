# 파일명: 검색기/modi_data.py

import utils
from typing import Any, Dict, List, Set, Union
import numpy as np
from datetime import datetime
from copy import deepcopy
from modi_morph_analyze import ModiMorphAnalyze
import os # os 모듈 추가
import logging # 로깅 추가

# 로거 설정
logger = logging.getLogger(__name__)
# 기본 로깅 레벨 설정 (app.py에서 이미 설정했다면 중복될 수 있으나 안전하게 추가)
if not logger.hasHandlers():
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- all3 설정 import ---
# app.py 에서 실행되는 환경을 기준으로 core.config 를 import 시도
# (app.py에서 sys.path에 '검색기'의 상위 폴더가 추가되어 있어야 함)
try:
    from core import config as app_config
    logger.info("all3/core/config.py (app_config) import 성공")
except ModuleNotFoundError:
    # 검색기 폴더에서 직접 실행 시 로컬 config 사용 (경고와 함께)
    try:
        import config as app_config # 검색기 로컬 config 사용
        logger.warning("Warning: all3/core/config.py 를 찾을 수 없어 검색기 로컬 config.py 사용")
    except ImportError:
        logger.error("CRITICAL: 설정 파일(config.py)을 찾을 수 없습니다. 경로 설정을 확인하세요.")
        # config 로드 실패 시 기본값 사용 또는 에러 발생 처리
        class FallbackConfig:
            HOT_KEYWORDS_DIR = './datas/docs' # 기본 저장 위치 (검색기/datas/docs)
            # 필요한 다른 설정값들도 정의
        app_config = FallbackConfig()
except Exception as e:
     logger.error(f"Config import 중 예상치 못한 오류: {e}", exc_info=True)
     raise # 설정 로드 실패는 심각한 문제일 수 있으므로 에러 발생시킴
# -----------------------


class ModiFashionData:
    def __init__(self):
        # 기본값 설정 추가
        self._doc_id: int = 0
        self._doc_type: str = ""
        self._original_id: int = 0
        self._title: str = ""
        self._content: str = ""
        self._source: str = ""
        self._url: str = ""
        self._published_date: str = ""
        self._created_at: str = ""
        self._processed: int = 0
        # doc_vec 타입을 List[float]로 일관성 유지 (특정 ID에 대한 벡터이므로)
        self._doc_vec: List[float] = []
        self._keywords: List[str] = []
        self._ent_vecs: List[List[float]] = []
        self._ent_vec_avg: List[float] = []


    def set_keywords(self, ma: ModiMorphAnalyze):
        self._keywords = ma.extract_nouns(self._title)
        self._keywords.extend(ma.extract_nouns(self._content))


    def to_dict(self) -> Dict[str, Any]:
        # 필요한 속성만 반환하도록 수정 (벡터 등 제외 가능)
        return {
            "id": getattr(self, '_doc_id', 0), # getattr로 안전하게 접근
            "doc_type": getattr(self, '_doc_type', ''),
            "original_id": getattr(self, '_original_id', 0),
            "title": getattr(self, '_title', ''),
            "content": getattr(self, '_content', ''),
            "source": getattr(self, '_source', ''),
            "url": getattr(self, '_url', ''),
            "published_date": getattr(self, '_published_date', ''),
            "created_at": getattr(self, '_created_at', ''),
            "processed": getattr(self, '_processed', 0),
            "doc_vec": getattr(self, '_doc_vec', []), # 벡터 필요시 포함
            "keywords": getattr(self, '_keywords', []),
            "ent_vecs": [], # 일반적으로 API 응답에는 포함하지 않음
            "ent_vec_avg": getattr(self, '_ent_vec_avg', []) # 필요시 포함
        }


class ModiMusinsaData:
    def __init__(self):
        # 기본값 설정 추가
        self._doc_id: int = 0
        self._product_id: int = 0
        self._brand: str = ""
        self._name: str = ""
        self._price: float = 0.0
        self._category: str = ""
        self._category_code: int = 0
        self._gender: str = ""
        self._rating: float = 0.0
        self._review_count: int = 0
        self._link: str = ""
        self._crawled_at: str = ""
        self._created_at: str = ""
        self._keywords: List[str] = []
        self._ent_vecs: List[List[float]] = []
        self._ent_vec_avg: List[float] = []


    def set_keywords(self, ma: ModiMorphAnalyze):
        self._keywords = ma.extract_nouns(self._brand)
        self._keywords.extend(ma.extract_nouns(self._name))
        self._keywords.extend(ma.extract_nouns(self._category))
        self._keywords.extend(ma.extract_nouns(self._gender))


    def to_dict(self) -> Dict[str, Any]:
        # 필요한 속성만 반환하도록 수정
        return {
            "id": getattr(self, '_doc_id', 0),
            "product_id": getattr(self, '_product_id', 0),
            "brand": getattr(self, '_brand', ''),
            "name": getattr(self, '_name', ''),
            "price": getattr(self, '_price', 0.0),
            "category": getattr(self, '_category', ''),
            "category_code": getattr(self, '_category_code', 0),
            "gender": getattr(self, '_gender', ''),
            "rating": getattr(self, '_rating', 0.0),
            "review_count": getattr(self, '_review_count', 0),
            "link": getattr(self, '_link', ''),
            "crawled_at": getattr(self, '_crawled_at', ''),
            "created_at": getattr(self, '_created_at', ''),
            "keywords": getattr(self, '_keywords', []),
            "ent_vecs": [], # 일반적으로 API 응답에는 포함하지 않음
            "ent_vec_avg": getattr(self, '_ent_vec_avg', []) # 필요시 포함
        }


def set_doc_vec(datas: List[ModiFashionData], doc_vecs: Dict[int, List[float]], dim=1024):
    # ... (이전 코드와 거의 동일, 로깅 및 기본값 처리 강화) ...
    default_vec = np.zeros(dim).tolist() # 미리 생성
    loaded_count = 0
    not_found_count = 0
    for data in datas:
        vec = doc_vecs.get(data._doc_id) # .get() 사용으로 Key 존재 여부 확인
        if vec and isinstance(vec, list) and len(vec) == dim:
             data._doc_vec = vec
             loaded_count += 1
        else:
             if vec is not None:
                  logger.warning(f"문서 ID {data._doc_id}의 벡터 차원({len(vec)})이 예상({dim})과 다릅니다. 제로 벡터 사용.")
             data._doc_vec = default_vec
             not_found_count += 1
    logger.info(f"문서 벡터 설정: 로드됨 {loaded_count}개, 찾을 수 없음/차원 오류 {not_found_count}개")


def set_ent_vec(datas: List[Union[ModiFashionData, ModiMusinsaData]], ent_vecs: Dict[str, List[float]], dim=1024):
    # ... (이전 코드와 거의 동일, 로깅 추가) ...
    if not ent_vecs:
         logger.warning("엔티티 벡터 데이터가 비어있어 엔티티 벡터 설정을 건너<0xEB><0x84><0x88니다.")
         return
    for data in datas:
        # 객체에 _keywords 속성이 있는지 확인
        if hasattr(data, '_keywords') and data._keywords:
             data._ent_vecs, data._ent_vec_avg = make_keyword_vecs(data._keywords, ent_vecs, dim)
        else:
             # 키워드가 없으면 빈 벡터 할당
             data._ent_vecs = []
             data._ent_vec_avg = np.zeros(dim).tolist()


def make_keyword_vecs(keywords: List[str], ent_vecs: Dict[str, List[float]], dim=1024):
    # ... (이전 코드와 거의 동일, 로깅 추가) ...
    keyword_vecs = []
    valid_vecs = []
    default_vec = np.zeros(dim).tolist()

    for keyword in keywords:
        vec = ent_vecs.get(keyword) # .get() 사용
        if vec and isinstance(vec, list) and len(vec) == dim:
            valid_vecs.append(vec)
            keyword_vecs.append(vec) # 원래 키워드 순서대로 벡터 저장 (유효하지 않으면 제로 벡터)
        else:
            keyword_vecs.append(default_vec) # 없는 경우 제로 벡터 추가
            if vec is not None: # 키는 있는데 값이 이상한 경우
                 logger.debug(f"키워드 '{keyword}'의 벡터 형식 또는 차원 오류")

    # 유효 벡터로만 평균 계산
    if not valid_vecs:
        keyword_vec_avg = default_vec
    else:
        try:
            keyword_vecs_arr = np.array(valid_vecs, dtype=np.float64) # 유효 벡터 사용
            keyword_vec_avg = np.mean(keyword_vecs_arr, axis=0).tolist()
        except Exception as e:
            logger.error(f"키워드 벡터 평균 계산 오류: {e}")
            keyword_vec_avg = default_vec

    return keyword_vecs, keyword_vec_avg


def data_list_to_dict_list(datas: List[Union[ModiFashionData, ModiMusinsaData]]):
    # ... (이전 코드와 거의 동일) ...
     return [data.to_dict() for data in datas]


class ModiData:
    # ... (ModiData 클래스 __init__, load_*, set_vec 내용은 이전과 거의 동일, 로깅 및 오류 처리 강화) ...
    def __init__(self):
        self._fashion_datas: List[ModiFashionData] = []
        self._musinsa_datas: List[ModiMusinsaData] = []
        self._doc_vecs: Dict[int, List[float]] = {}
        self._ent_vecs: Dict[str, List[float]] = {}

    def load_fashion(self, in_file_path: str, encoding='UTF-8', ma: ModiMorphAnalyze = None):
        if not utils.file_exists(in_file_path):
             logger.error(f"패션 데이터 파일 없음: {in_file_path}")
             return
        json_dicts = utils.load_json_file_to_dict(in_file_path, encoding)
        if json_dicts is None:
             logger.error(f"패션 데이터 로드 실패 (JSON 오류?): {in_file_path}")
             return
        logger.info(f'ModiData.load_fashion() in_file_path : {in_file_path}, data size : {len(json_dicts)}')

        loaded_count = 0
        for json_dict in json_dicts:
            try: # 개별 데이터 로딩 오류 처리
                 fashion_data = ModiFashionData()
                 fashion_data._doc_id = int(json_dict['id'])
                 fashion_data._doc_type = str(json_dict.get('doc_type', 'unknown'))
                 fashion_data._original_id = int(json_dict['original_id'])
                 fashion_data._title = str(json_dict.get('title', ''))
                 fashion_data._content = str(json_dict.get('content', ''))
                 fashion_data._source = str(json_dict.get('source', ''))
                 fashion_data._url = str(json_dict.get('url', ''))
                 fashion_data._published_date = str(json_dict.get('published_date', ''))
                 fashion_data._created_at = str(json_dict.get('created_at', '')) # 날짜 형식은 여기서 신경쓰지 않음
                 fashion_data._processed = int(json_dict.get('processed', 0))

                 if ma is not None:
                     fashion_data.set_keywords(ma) # 로딩 시 키워드 추출

                 self._fashion_datas.append(fashion_data)
                 loaded_count += 1
            except KeyError as ke:
                 logger.warning(f"패션 데이터 로딩 중 누락된 키: {ke} - 데이터 건너<0xEB><0x84><0x88니다. ID: {json_dict.get('id')}")
            except Exception as e:
                 logger.error(f"패션 데이터 처리 중 오류: {e} - 데이터 건너<0xEB><0x84><0x88니다. ID: {json_dict.get('id')}", exc_info=True)
        logger.info(f'ModiData.load_fashion() 로드된 패션 데이터 수 : {loaded_count}\n')

    def load_musinsa(self, in_file_path: str, encoding='UTF-8', ma: ModiMorphAnalyze = None):
        if not utils.file_exists(in_file_path):
             logger.error(f"무신사 데이터 파일 없음: {in_file_path}")
             return
        json_dicts = utils.load_json_file_to_dict(in_file_path, encoding)
        if json_dicts is None:
             logger.error(f"무신사 데이터 로드 실패 (JSON 오류?): {in_file_path}")
             return
        logger.info(f'ModiData.load_musinsa() in_file_path : {in_file_path}, data size : {len(json_dicts)}')

        loaded_count = 0
        for json_dict in json_dicts:
            try: # 개별 데이터 로딩 오류 처리
                 musinsa_data = ModiMusinsaData()
                 musinsa_data._doc_id = int(json_dict['id'])
                 musinsa_data._product_id = int(json_dict['product_id'])
                 musinsa_data._brand = str(json_dict.get('brand', ''))
                 musinsa_data._name = str(json_dict.get('name', ''))
                 # 가격 처리 주의
                 price_raw = json_dict.get('price', 0)
                 if isinstance(price_raw, str):
                     try: musinsa_data._price = float(price_raw.replace('원', '').replace(',', '').strip())
                     except ValueError: musinsa_data._price = 0.0
                 else: musinsa_data._price = float(price_raw)

                 musinsa_data._category = str(json_dict.get('category', ''))
                 musinsa_data._category_code = int(json_dict.get('category_code', 0))
                 musinsa_data._gender = str(json_dict.get('gender', ''))
                 musinsa_data._rating = float(json_dict.get('rating', 0.0))
                 musinsa_data._review_count = int(json_dict.get('review_count', 0))
                 musinsa_data._link = str(json_dict.get('link', ''))
                 musinsa_data._crawled_at = str(json_dict.get('crawled_at', '')) # 날짜 형식은 여기서 신경쓰지 않음
                 musinsa_data._created_at = str(json_dict.get('created_at', ''))

                 if ma is not None:
                     musinsa_data.set_keywords(ma) # 로딩 시 키워드 추출

                 self._musinsa_datas.append(musinsa_data)
                 loaded_count += 1
            except KeyError as ke:
                 logger.warning(f"무신사 데이터 로딩 중 누락된 키: {ke} - 데이터 건너<0xEB><0x84><0x88니다. ID: {json_dict.get('id')}")
            except Exception as e:
                 logger.error(f"무신사 데이터 처리 중 오류: {e} - 데이터 건너<0xEB><0x84><0x88니다. ID: {json_dict.get('id')}", exc_info=True)

        logger.info(f'ModiData.load_musinsa() 로드된 무신사 데이터 수 : {loaded_count}\n')


    def load_doc_vecs(self, in_file_path: str, encoding='UTF-8'):
        # ... (이전 답변의 로깅 및 오류 처리 강화 버전 유지) ...
        if not utils.file_exists(in_file_path):
             logger.error(f"문서 벡터 파일 없음: {in_file_path}")
             self._doc_vecs = {} # 빈 딕셔너리로 초기화
             return
        json_dicts = utils.load_json_file_to_dict(in_file_path, encoding)
        if json_dicts is None:
             logger.error(f"문서 벡터 로드 실패 (JSON 오류?): {in_file_path}")
             self._doc_vecs = {}
             return
        # ... (이하 벡터 처리 및 로깅 코드 - 이전 답변 참고) ...
        loaded_vectors = 0
        vec_dim = None
        temp_doc_vecs = {} # 임시 딕셔너리 사용
        for json_dict in json_dicts:
            try:
                key = int(json_dict['doc_id'])
                value = json_dict.get('embedding') # .get() 사용

                if value is None:
                     logger.warning(f"doc_id {key}의 embedding 필드 없음, 건너<0xEB><0x84><0x88니다.")
                     continue

                # 문자열 벡터 처리 (이전 코드 유지)
                if isinstance(value, str):
                    value = value.strip('[]"')
                    value = [float(x.strip()) for x in value.split(',')]

                if isinstance(value, list) and value: # 리스트이고 비어있지 않은지 확인
                    current_dim = len(value)
                    if vec_dim is None: # 첫 벡터 차원 저장
                         vec_dim = current_dim
                    if current_dim == vec_dim: # 차원 일치 확인
                         temp_doc_vecs[key] = value
                         loaded_vectors += 1
                    else:
                         logger.warning(f"doc_id {key}의 벡터 차원({current_dim})이 예상({vec_dim})과 다름, 건너<0xEB><0x84><0x88니다.")
                else:
                    logger.warning(f"doc_id {key}의 벡터 형식이 잘못되었거나 비어있음, 건너<0xEB><0x84><0x88니다.")

            except Exception as e:
                logger.error(f"Error processing doc_vec for doc_id: {json_dict.get('doc_id', 'unknown')}, error: {e}", exc_info=True)

        self._doc_vecs = temp_doc_vecs # 최종 결과 할당
        logger.info(f"로드된 문서 벡터: {loaded_vectors}개")

        # 벡터 로드 실패 시 더미 벡터 생성 로직은 제거 (set_vec에서 처리)
        if self._doc_vecs:
             first_vec_key = next(iter(self._doc_vecs))
             emb_dim = len(self._doc_vecs[first_vec_key])
             logger.info(f'ModiData.load_doc_vecs() data size : {len(self._doc_vecs)}, emb_dim : {emb_dim}')
        else:
             logger.info('ModiData.load_doc_vecs() 로딩된 벡터 없음')


    def load_ent_vecs(self, in_file_path: str, encoding='UTF-8'):
        # ... (load_doc_vecs 와 유사하게 수정) ...
        if not utils.file_exists(in_file_path):
             logger.error(f"엔티티 벡터 파일 없음: {in_file_path}")
             self._ent_vecs = {}
             return
        json_dicts = utils.load_json_file_to_dict(in_file_path, encoding)
        if json_dicts is None:
             logger.error(f"엔티티 벡터 로드 실패 (JSON 오류?): {in_file_path}")
             self._ent_vecs = {}
             return
        # ... (이하 벡터 처리 및 로깅 코드 - 이전 답변 참고) ...
        loaded_vectors = 0
        vec_dim = None
        temp_ent_vecs = {}
        for json_dict in json_dicts:
            try:
                key = json_dict.get('ent')
                value = json_dict.get('embedding')

                if not key or value is None:
                     logger.warning("엔티티 또는 embedding 필드 없음, 건너<0xEB><0x84><0x88니다.")
                     continue

                # 문자열 벡터 처리
                if isinstance(value, str):
                    value = value.strip('[]"')
                    value = [float(x.strip()) for x in value.split(',')]

                if isinstance(value, list) and value:
                    current_dim = len(value)
                    if vec_dim is None: vec_dim = current_dim
                    if current_dim == vec_dim:
                        temp_ent_vecs[key] = value
                        loaded_vectors += 1
                    else:
                        logger.warning(f"엔티티 '{key}'의 벡터 차원({current_dim})이 예상({vec_dim})과 다름, 건너<0xEB><0x84><0x88니다.")
                else:
                     logger.warning(f"엔티티 '{key}'의 벡터 형식이 잘못되었거나 비어있음, 건너<0xEB><0x84><0x88니다.")

            except Exception as e:
                logger.error(f"Error processing ent_vec for ent: {json_dict.get('ent', 'unknown')}, error: {e}", exc_info=True)

        self._ent_vecs = temp_ent_vecs
        logger.info(f"로드된 엔티티 벡터: {loaded_vectors}개")

        if self._ent_vecs:
             first_ent_key = next(iter(self._ent_vecs))
             emb_dim = len(self._ent_vecs[first_ent_key])
             logger.info(f'ModiData.load_ent_vecs() data size : {len(self._ent_vecs)}, emb_dim : {emb_dim}')
        else:
             logger.info('ModiData.load_ent_vecs() 로딩된 벡터 없음')


    def set_vec(self):
        logger.info("문서 및 엔티티 벡터 설정 시작...")
        # 벡터 데이터 로드 확인 및 기본 차원 설정
        doc_vec_dim = 1024 # 기본 차원
        if self._doc_vecs:
            try:
                 doc_vec_dim = len(next(iter(self._doc_vecs.values())))
            except StopIteration:
                 logger.warning("문서 벡터 데이터는 있으나 비어있습니다.")
            except TypeError:
                 logger.error("문서 벡터 데이터 형식이 잘못되었습니다.")

        ent_vec_dim = 1024 # 기본 차원
        if self._ent_vecs:
            try:
                 ent_vec_dim = len(next(iter(self._ent_vecs.values())))
            except StopIteration:
                 logger.warning("엔티티 벡터 데이터는 있으나 비어있습니다.")
            except TypeError:
                 logger.error("엔티티 벡터 데이터 형식이 잘못되었습니다.")

        set_doc_vec(self._fashion_datas, self._doc_vecs, dim=doc_vec_dim)
        set_ent_vec(self._fashion_datas, self._ent_vecs, dim=ent_vec_dim)
        set_ent_vec(self._musinsa_datas, self._ent_vecs, dim=ent_vec_dim)
        logger.info("문서 및 엔티티 벡터 설정 완료.")

    # ==============================================================
    # ============= 핫 키워드 생성 함수 (경로 수정됨) ===============
    # ==============================================================
    def make_hot_keywords(self, start_date: str, end_date: str, filter_len: int, output_path: str, ma: ModiMorphAnalyze = None):
        """지정된 기간의 패션 데이터에서 핫 키워드를 추출하고 파일로 저장합니다."""
        # --- 날짜 변환 로직 ---
        start_date_obj, end_date_obj = None, None
        date_formats_to_try = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"] # 시도할 날짜 형식 목록
        try:
            # 입력 날짜 파싱
            for fmt in date_formats_to_try:
                try: start_date_obj = datetime.strptime(start_date, fmt); break
                except ValueError: continue
            if start_date_obj is None: raise ValueError(f"시작 날짜 형식 변환 실패: {start_date}")

            for fmt in date_formats_to_try:
                try:
                    end_date_obj = datetime.strptime(end_date, fmt)
                    if fmt == "%Y-%m-%d": end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)
                    break
                except ValueError: continue
            if end_date_obj is None: raise ValueError(f"종료 날짜 형식 변환 실패: {end_date}")

        except ValueError as e:
            logger.error(f"핫 키워드 날짜 형식 오류: {e}")
            return None
        # --- 날짜 변환 끝 ---

        searched = []
        logger.info(f"핫 키워드 필터링 시작: 기간 [{start_date_obj} ~ {end_date_obj}]")
        processed_ids = set()

        date_field_to_use = '_created_at' # 기본적으로 _created_at 사용
        # _created_at 이 없거나 비어있는 경우 _published_date 사용 시도 (예시)
        # if not all(hasattr(d, '_created_at') and d._created_at for d in self._fashion_datas):
        #     date_field_to_use = '_published_date'
        #     logger.info(f"_created_at 필드 문제로 '{date_field_to_use}' 필드를 사용하여 필터링합니다.")

        parse_failures = 0
        comparison_errors = 0
        no_date_info = 0

        for data in self._fashion_datas:
            if data._doc_id in processed_ids: continue

            created_date = None
            date_string_to_parse = getattr(data, date_field_to_use, None) # 사용할 날짜 필드 가져오기

            if not date_string_to_parse:
                no_date_info += 1
                continue

            for fmt in date_formats_to_try:
                try:
                    created_date = datetime.strptime(date_string_to_parse, fmt)
                    # 날짜만 있는 형식 파싱 시 시간 정보 추가 (00:00:00)
                    if fmt == "%Y-%m-%d":
                         created_date = created_date.replace(hour=0, minute=0, second=0)
                    break
                except ValueError:
                    continue

            if created_date:
                try:
                    # 시간대 정보 없는 naive datetime으로 비교 통일
                    if start_date_obj.tzinfo is not None: start_date_obj = start_date_obj.replace(tzinfo=None)
                    if end_date_obj.tzinfo is not None: end_date_obj = end_date_obj.replace(tzinfo=None)
                    if created_date.tzinfo is not None: created_date = created_date.replace(tzinfo=None)

                    if start_date_obj <= created_date <= end_date_obj:
                        searched.append(deepcopy(data))
                        processed_ids.add(data._doc_id)
                except Exception as comp_e:
                     comparison_errors += 1
                     logger.debug(f"ID {data._doc_id}: 날짜 비교 중 오류 ({comp_e}), 건너<0xEB><0x84><0x88니다.")
            else:
                 parse_failures += 1
                 logger.debug(f"ID {data._doc_id}: 날짜 '{date_string_to_parse}' 형식 변환 실패, 건너<0xEB><0x84><0x88니다.")

        logger.info(f'ModiData.make_hot_keywords() date : [{start_date_obj} ~ {end_date_obj}], searched : {len(searched)}')
        if parse_failures > 0: logger.warning(f"날짜 형식 변환 실패 건수: {parse_failures}")
        if comparison_errors > 0: logger.warning(f"날짜 비교 오류 건수: {comparison_errors}")
        if no_date_info > 0: logger.warning(f"날짜 정보 누락 건수: {no_date_info}")

        if not searched:
            logger.warning("해당 기간에 필터링된 문서가 없습니다. 날짜 형식 또는 기간을 확인하세요.")
            # 데이터가 없더라도 빈 딕셔너리 반환하도록 수정 (더미 생성 대신)
            return {} # 빈 딕셔너리 반환


        all_keywords = {}
        if ma is None:
            logger.error("형태소 분석기가 제공되지 않아 키워드를 추출할 수 없습니다.")
            return {} # 빈 딕셔너리 반환

        for data in searched:
            if not hasattr(data, '_keywords') or not data._keywords:
                 data.set_keywords(ma)
            # data._keywords가 리스트인지 확인
            if isinstance(data._keywords, list):
                 utils.add_str_list_int(all_keywords, data._keywords, 1)
            else:
                 logger.warning(f"ID {data._doc_id}: 키워드가 리스트 형식이 아님 ({type(data._keywords)}), 건너<0xEB><0x84><0x88니다.")


        logger.info(f'ModiData.make_hot_keywords() keyword size : {len(all_keywords)}')

        filtered_keywords = {key: value for key, value in all_keywords.items() if len(key) >= filter_len}
        logger.info(f'ModiData.make_hot_keywords() filtered keyword size : {len(filtered_keywords)}')

        if len(filtered_keywords) > 0:
            sorted_keywords = utils.sorted_dict(filtered_keywords)

            # --- 파일 경로 생성 및 저장 부분 (수정됨) ---
            try:
                # 직접 전달받은 output_path 사용
                if output_path:
                    # output_path의 디렉토리 부분 확인 및 생성
                    output_dir = os.path.dirname(output_path)
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)

                    # 수정된 경로로 파일 저장
                    if utils.write_json_file(sorted_keywords, output_path):
                        logger.info(f"핫 키워드 저장 성공: {output_path}")
                    else:
                        logger.error(f"핫 키워드 저장 실패 (write_json_file 실패): {output_path}")
                else:
                    # output_path가 없는 경우 config 사용 (기존 로직)
                    if hasattr(app_config, 'HOT_KEYWORDS_DIR') and app_config.HOT_KEYWORDS_DIR and os.path.isdir(app_config.HOT_KEYWORDS_DIR):
                        # 파일 이름 생성
                        filename = f"hot_keywords_{start_date_obj.strftime('%Y-%m-%d')}-{end_date_obj.strftime('%Y-%m-%d')}.json"
                        # os.path.join을 사용하여 전체 경로 생성
                        output_filepath = os.path.join(app_config.HOT_KEYWORDS_DIR, filename)

                        # 디렉토리 존재 확인 및 생성 (이미 확인되었지만 안전하게)
                        os.makedirs(app_config.HOT_KEYWORDS_DIR, exist_ok=True)

                        # 수정된 경로로 파일 저장
                        if utils.write_json_file(sorted_keywords, output_filepath):
                            logger.info(f"핫 키워드 저장 성공: {output_filepath}")
                        else:
                            logger.error(f"핫 키워드 저장 실패 (write_json_file 실패): {output_filepath}")
                    else:
                        logger.error(f"Config 파일의 HOT_KEYWORDS_DIR('{getattr(app_config, 'HOT_KEYWORDS_DIR', '미정의')}')이 유효한 디렉토리가 아닙니다. 파일 저장 실패.")
                        # 저장 실패해도 키워드는 반환

            except AttributeError as ae:
                 logger.error(f"### error utils.write_json_file() 경로 생성 오류: config 파일에 HOT_KEYWORDS_DIR 정의 확인 필요 - {ae}")
            except Exception as e:
                 logger.error(f"### error utils.write_json_file() 파일 쓰기 오류: {e}", exc_info=True)
                 logger.error(f"시도한 경로: {output_filepath if 'output_filepath' in locals() else '경로 생성 실패'}")
                 if isinstance(e, PermissionError):
                     logger.error("### 해당 경로에 쓰기 권한이 있는지 확인하세요.")
            # --- 수정 끝 ---

            return sorted_keywords
        else:
            logger.warning("필터링 후 남은 핫 키워드가 없습니다.")
            return {} # 빈 딕셔너리 반환
    # ==============================================================


########################################################################################################################################################


if __name__ == "__main__" :
    # 이 부분은 직접 실행 시 사용되므로, all3 프로젝트와는 별개로 동작
    print("--- Running modi_data.py as main script ---")
    local_data_dir = './datas'
    if not os.path.isdir(local_data_dir): # datas 폴더가 없으면 생성
         os.makedirs(local_data_dir)
         os.makedirs(os.path.join(local_data_dir, 'docs'), exist_ok=True)
         os.makedirs(os.path.join(local_data_dir, 'vecs'), exist_ok=True)
         print(f"Created local '{local_data_dir}' structure for testing.")

    docs_dir, vecs_dir = os.path.join(local_data_dir, 'docs'), os.path.join(local_data_dir, 'vecs')

    modi_data = ModiData()
    modi_ma = ModiMorphAnalyze()

    # 로컬 테스트용 파일 경로 (실제 파일 필요)
    fashion_file = os.path.join(docs_dir, 'fashion_document_raw.json')
    musinsa_file = os.path.join(docs_dir, 'musinsa_raw.json')
    doc_vec_file = os.path.join(vecs_dir, 'doc_vec.json') # 실제 파일명으로 변경 필요
    ent_vec_file = os.path.join(vecs_dir, 'ent_vec.json') # 실제 파일명으로 변경 필요

    # 로컬 테스트 파일 생성 (임시 - 내용 없는 빈 JSON)
    for f_path in [fashion_file, musinsa_file, doc_vec_file, ent_vec_file]:
         if not os.path.exists(f_path):
             try:
                 with open(f_path, 'w', encoding='utf-8') as f:
                     f.write('[]') # 빈 JSON 배열
                 print(f"Created dummy file: {f_path}")
             except IOError as e:
                 print(f"Error creating dummy file {f_path}: {e}")


    modi_data.load_fashion(fashion_file, ma=modi_ma)
    modi_data.load_musinsa(musinsa_file, ma=modi_ma)
    modi_data.load_doc_vecs(doc_vec_file)
    modi_data.load_ent_vecs(ent_vec_file)

    # 벡터 설정 전에 벡터가 로드되었는지 확인
    if modi_data._doc_vecs and modi_data._ent_vecs:
         modi_data.set_vec()
         # 벡터 포함 파일 저장 (로컬 실행용)
         fashion_out_file = os.path.join(docs_dir, 'fashion_document_raw_vecs.json')
         musinsa_out_file = os.path.join(docs_dir, 'musinsa_raw_vecs.json')
         utils.write_json_file(data_list_to_dict_list(modi_data._fashion_datas), fashion_out_file)
         utils.write_json_file(data_list_to_dict_list(modi_data._musinsa_datas), musinsa_out_file)
    else:
         print("벡터 데이터가 로드되지 않아 set_vec 및 파일 저장을 건너<0xEB><0x84><0x88니다.")

    # 데이터의 날짜 확인
    dates = []
    for data in modi_data._fashion_datas[:10]:
        # 안전하게 속성 접근
        doc_id = getattr(data, '_doc_id', 'N/A')
        created_at = getattr(data, '_created_at', 'N/A')
        print(f"데이터 ID: {doc_id}, 생성일: {created_at}")
        if created_at != 'N/A':
            dates.append(created_at)
    print(f"날짜 샘플: {dates}")

    # 핫 키워드 (로컬 실행용)
    from datetime import datetime, timedelta # timedelta 추가
    start_date_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 수정된 make_hot_keywords 호출 (out_file_path 인자 제거됨)
    # 로컬 실행 시 config.py import가 실패할 수 있으므로, app_config.HOT_KEYWORDS_DIR 대신
    # 로컬 경로(docs_dir)를 사용하도록 직접 수정하거나, 로컬 테스트용 config 로직 강화 필요
    # 여기서는 app_config 가 임시로 로드되었다고 가정하고 호출 시도
    try:
         print(f"\n--- 로컬 핫 키워드 생성 테스트 시작 ({start_date_str} ~ {end_date_str}) ---")
         hot_keywords_result = modi_data.make_hot_keywords(start_date_str, end_date_str, filter_len=4, output_path=os.path.join(docs_dir, 'hot_keywords.json'), ma=modi_ma)
         if hot_keywords_result:
              print("로컬 핫 키워드 생성 결과:", hot_keywords_result)
         else:
              print("로컬 핫 키워드 생성 결과 없음.")
         print("--- 로컬 핫 키워드 생성 테스트 끝 ---")
    except Exception as e:
         print(f"로컬 핫 키워드 생성 테스트 중 오류: {e}")

    print("\n--- modi_data.py main script finished ---")

