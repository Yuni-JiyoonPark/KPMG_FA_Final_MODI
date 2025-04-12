# 파일명: core/db_connector.py

import mysql.connector
from mysql.connector import pooling
import pandas as pd
import os
import logging
# config 파일을 정확히 참조하도록 수정 (상대 경로 사용)
# config 파일에 PERIOD_DAYS가 정의되어 있다고 가정합니다.
from .config import DB_CONFIG, PERIOD_DAYS

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DBConnector:
    """데이터베이스 연결 및 쿼리 실행을 담당하는 클래스"""

    _connection_pool = None

    @classmethod
    def get_connection_pool(cls):
        """연결 풀 반환 (없으면 생성)"""
        if cls._connection_pool is None:
            try:
                cls._connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="fashion_trend_pool",
                    pool_size=5,  # 연결 풀 크기 조정
                    **DB_CONFIG # core/config.py의 DB_CONFIG 사용
                )
                logger.info("DB 연결 풀 생성 완료")
            except Exception as e:
                logger.error(f"Connection pool 생성 실패: {e}")
                return None
        return cls._connection_pool

    @staticmethod
    def get_connection():
        """MySQL 연결 객체 반환"""
        try:
            pool = DBConnector.get_connection_pool()
            if pool:
                connection = pool.get_connection()
                logger.debug("DB 연결 풀에서 연결 가져옴")
                return connection
            else:
                logger.warning("연결 풀 사용 불가, 직접 연결 시도")
                conn = mysql.connector.connect(**DB_CONFIG) # core/config.py의 DB_CONFIG 사용
                return conn
        except mysql.connector.Error as err:
            logger.error(f"MySQL 연결 오류: {err}")
            return None

    @staticmethod
    def test_connection():
        """데이터베이스 연결 테스트"""
        conn = None
        cursor = None
        try:
            conn = DBConnector.get_connection()
            if not conn:
                logger.error("연결 객체를 가져올 수 없습니다.")
                return False

            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

            if result and result[0] == 1:
                logger.info("데이터베이스 연결 테스트 성공")
                return True
            else:
                logger.warning("데이터베이스 연결 테스트 결과가 예상과 다릅니다.")
                return False
        except Exception as e:
            logger.error(f"연결 테스트 실패: {e}")
            return False
        finally:
             try:
                 if cursor: cursor.close()
                 if conn and conn.is_connected(): conn.close()
             except Exception as e: logger.error(f"테스트 연결 종료 오류: {e}")


    @staticmethod
    def execute_query(query, params=None, fetch=True):
        """
        쿼리 실행 및 결과 반환
        """
        conn = None
        cursor = None
        try:
            conn = DBConnector.get_connection()
            if not conn:
                logger.error("데이터베이스 연결 실패")
                return None if fetch else False

            # 파라미터가 None일 경우 빈 튜플로 처리 (mysql.connector 요구사항)
            params = params or ()

            if fetch:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params)
                rows = cursor.fetchall()
                if rows:
                    return pd.DataFrame(rows)
                logger.warning(f"쿼리 결과 없음: {query[:100]}...")
                return pd.DataFrame() # 빈 DataFrame 반환
            else:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                logger.info(f"쿼리 실행 완료 (non-fetch): {query[:100]}...")
                return True
        except mysql.connector.Error as err:
            logger.error(f"쿼리 실행 DB 오류: {err} (쿼리: {query[:200]}..., 파라미터: {params})")
            if not fetch and conn:
                try: conn.rollback()
                except Exception as rb_err: logger.error(f"롤백 오류: {rb_err}")
            return None if fetch else False
        except Exception as e:
            logger.error(f"쿼리 실행 중 예상치 못한 오류: {e} (쿼리: {query[:200]}...)", exc_info=True)
            if not fetch and conn:
                try: conn.rollback()
                except Exception as rb_err: logger.error(f"롤백 오류: {rb_err}")
            return None if fetch else False
        finally:
            try:
                 if cursor: cursor.close()
                 if conn and conn.is_connected(): conn.close()
            except Exception as e: logger.error(f"쿼리 실행 연결 종료 오류: {e}")

    @staticmethod
    def load_magazine_data(domain=None, source=None, start_date=None, end_date=None, limit=None):
        """
        매거진 또는 뉴스 토큰화 데이터 로드
        !!! 중요: 테이블 이름과 날짜 컬럼(upload_date)이 실제 DB와 맞는지 확인 필요 !!!
        """
        try:
            table_name = "fashion_trends.magazine_tokenised" # 실제 테이블 이름 확인 필요
            date_column = "upload_date" # 실제 날짜 컬럼 이름 확인 필요

            query = f"SELECT id, doc_domain, {date_column}, tokens, source FROM {table_name}"

            conditions = []
            params = []

            if domain:
                conditions.append("doc_domain = %s")
                params.append(domain)
            if source:
                conditions.append("source = %s")
                params.append(source)
            if start_date:
                conditions.append(f"DATE({date_column}) >= DATE(%s)")
                params.append(start_date)
            if end_date:
                conditions.append(f"DATE({date_column}) <= DATE(%s)")
                params.append(end_date)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" ORDER BY {date_column} DESC"

            limit_val = int(limit) if limit else 1000
            query += " LIMIT %s"
            params.append(limit_val)

            logger.info(f"매거진/뉴스 데이터 로드 쿼리: {query[:200]}..., 파라미터: {params}")
            df = DBConnector.execute_query(query, tuple(params)) # params를 튜플로 전달

            if df is not None and not df.empty:
                # 토큰 변환
                if 'tokens' in df.columns:
                    import json
                    def safe_json_loads(x):
                        try: return json.loads(x) if isinstance(x, str) else (x if isinstance(x, list) else [])
                        except (json.JSONDecodeError, TypeError): return []
                    df['tokens'] = df['tokens'].apply(safe_json_loads)
                else:
                     df['tokens'] = [[] for _ in range(len(df))]

                # 날짜 변환
                if date_column in df.columns:
                    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
                    original_len = len(df)
                    df.dropna(subset=[date_column], inplace=True)
                    if len(df) < original_len:
                         logger.warning(f"{original_len - len(df)}개의 행이 날짜 변환 실패로 제거됨 ({date_column})")
                    if df.empty:
                         logger.warning(f"날짜 변환 후 유효한 매거진/뉴스 데이터가 없습니다 ({date_column}).")
                         return pd.DataFrame(columns=['id', 'doc_domain', date_column, 'tokens', 'source'])
                else:
                     logger.warning(f"예상된 날짜 컬럼({date_column})이 매거진/뉴스 데이터에 없습니다.")

                logger.info(f"{domain if domain else '매거진/뉴스'} 데이터 {len(df)}개 로드 완료")
            else:
                logger.warning(f"{domain if domain else '매거진/뉴스'} 데이터가 없습니다.")
                # 컬럼 이름 일관성 유지
                df = pd.DataFrame(columns=['id', 'doc_domain', date_column, 'tokens', 'source'])

            return df
        except Exception as e:
            logger.error(f"매거진/뉴스 데이터 로드 오류: {e}", exc_info=True)
            return pd.DataFrame(columns=['id', 'doc_domain', 'upload_date', 'tokens', 'source'])


    @staticmethod
    def get_magazine_sources():
        """매거진 출처 목록 가져오기 (테이블 이름 확인 필요)"""
        # !!! 중요: magazine_tokenised 테이블 이름 확인 필요 !!!
        table_name = "fashion_trends.magazine_tokenised"
        query = f"SELECT DISTINCT source FROM {table_name} WHERE doc_domain = '매거진' ORDER BY source"
        try:
            df = DBConnector.execute_query(query)
            return df['source'].tolist() if df is not None and not df.empty else []
        except Exception as e:
            logger.error(f"매거진 출처 목록 가져오기 오류: {e}", exc_info=True)
            return []

    @staticmethod
    def get_magazines_in_period(period):
        """특정 기간 내 매거진 목록 가져오기 (테이블 및 날짜 컬럼 확인 필요)"""
        # !!! 중요: magazine_tokenised 테이블 및 날짜 컬럼 확인 필요 !!!
        table_name = "fashion_trends.magazine_tokenised"
        date_column = "upload_date"
        from datetime import datetime, timedelta
        try:
            today = datetime.now()
            days = PERIOD_DAYS.get(period) # config 에서 PERIOD_DAYS 사용

            if days:
                start_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')

                query = f"""
                SELECT DISTINCT source FROM {table_name}
                WHERE doc_domain = '매거진' AND DATE({date_column}) BETWEEN DATE(%s) AND DATE(%s)
                ORDER BY source
                """
                params = (start_date, end_date) # 튜플로 전달
                df = DBConnector.execute_query(query, params)

                if df is not None and not df.empty:
                    return df['source'].tolist()
                else:
                    logger.warning(f"{period} 기간 동안 매거진 출처 데이터가 없습니다.")
                    return []
            else:
                logger.warning(f"get_magazines_in_period: 지원하지 않는 기간: {period}")
                return DBConnector.get_magazine_sources() # 전체 목록 반환
        except Exception as e:
            logger.error(f"기간별 매거진 목록 가져오기 오류: {e}", exc_info=True)
            return []

    @staticmethod
    def get_news_data(period=None, start_date=None, end_date=None, limit=None):
        """뉴스 데이터 로드 (load_magazine_data 호출)"""
        # load_magazine_data 함수는 period 인자를 직접 받지 않으므로,
        # 날짜 계산이 필요하면 호출 전에 미리 계산해서 start_date, end_date로 전달해야 함.
        # 여기서는 일단 그대로 전달
        return DBConnector.load_magazine_data(
            domain='뉴스',
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

    # ==============================================================
    # ============= 무신사 데이터 로딩 함수 (수정 반영) =============
    # ==============================================================
    @staticmethod
    def get_musinsa_data(limit=1000, period=None, start_date=None, end_date=None):
        """무신사 데이터를 DB에서 가져오기 (테이블명 및 날짜컬럼 수정)"""
        conn = None
        cursor = None
        try:
            conn = DBConnector.get_connection()
            if not conn:
                 logger.error("get_musinsa_data: 데이터베이스 연결 실패")
                 return pd.DataFrame()

            cursor = conn.cursor(dictionary=True)

            # --- 테이블 이름 수정 ---
            table_name = "fashion_trends.musinsa_products"
            query = f"""
                SELECT * FROM {table_name}
                WHERE 1=1
            """
            # --- 수정 끝 ---

            params = []
            # !!! 중요: 실제 musinsa_products2 테이블의 날짜 컬럼 이름으로 수정 !!!
            actual_date_column = 'crawled_at' # 예시, 실제 컬럼 이름으로 바꾸세요!

            # 기간 또는 날짜 범위 필터링
            if start_date and end_date:
                query += f" AND DATE({actual_date_column}) BETWEEN DATE(%s) AND DATE(%s)"
                params.extend([start_date, end_date])
                logger.info(f"Musinsa Data Filter: Date range {start_date} to {end_date}")
            elif period:
                # 기간 계산
                from datetime import date, timedelta
                days = PERIOD_DAYS.get(period) # config에서 PERIOD_DAYS 사용
                if days:
                     calculated_start_date = (date.today() - timedelta(days=days)).strftime('%Y-%m-%d')
                     query += f" AND DATE({actual_date_column}) >= DATE(%s)"
                     params.append(calculated_start_date)
                     logger.info(f"Musinsa Data Filter: Period {period} (from {calculated_start_date})")
                else:
                     logger.warning(f"get_musinsa_data: 유효하지 않은 기간 값: {period}")
            elif start_date: # start_date만 있는 경우
                 query += f" AND DATE({actual_date_column}) >= DATE(%s)"
                 params.append(start_date)
                 logger.info(f"Musinsa Data Filter: Start date {start_date}")
            elif end_date: # end_date만 있는 경우
                 query += f" AND DATE({actual_date_column}) <= DATE(%s)"
                 params.append(end_date)
                 logger.info(f"Musinsa Data Filter: End date {end_date}")


            # 정렬 및 제한
            query += f" ORDER BY {actual_date_column} DESC" # 실제 날짜 컬럼 사용

            # LIMIT 값은 정수여야 함
            limit_val = int(limit) if limit else 1000
            query += " LIMIT %s"
            params.append(limit_val)

            logger.info(f"무신사 데이터 로드 쿼리: {query[:200]}..., 파라미터: {params}")

            # 쿼리 실행
            cursor.execute(query, tuple(params)) # params를 튜플로 전달
            result = cursor.fetchall()

            # 결과 처리
            if result:
                df = pd.DataFrame(result)
                # 날짜 형식 변환 (실제 날짜 컬럼 사용)
                if actual_date_column in df.columns:
                     df[actual_date_column] = pd.to_datetime(df[actual_date_column], errors='coerce')
                     original_len = len(df)
                     df.dropna(subset=[actual_date_column], inplace=True)
                     if len(df) < original_len:
                          logger.warning(f"{original_len - len(df)}개의 행이 날짜 변환 실패로 제거됨 ({actual_date_column})")
                     if df.empty:
                         logger.warning(f"날짜 변환 후 유효한 무신사 데이터가 없습니다 ({actual_date_column}).")
                         return pd.DataFrame(columns=df.columns) # 원래 컬럼 유지하며 빈 DF 반환
                else:
                     logger.warning(f"무신사 데이터에 예상된 날짜 컬럼({actual_date_column})이 없습니다.")
                     # 날짜 컬럼 없어도 일단 반환
                logger.info(f"무신사 데이터 로드 성공: {len(df)} 건")
                return df
            else:
                logger.warning("무신사 데이터가 없습니다.")
                return pd.DataFrame()

        except mysql.connector.Error as err:
             logger.error(f"무신사 데이터 로드 DB 오류: {err}")
             if err.errno == 1146: logger.error(f"오류: '{table_name}' 테이블이 DB에 존재하지 않습니다.")
             elif err.errno == 1054: logger.error(f"오류: SQL 쿼리에 잘못된 컬럼 이름이 사용되었습니다. (예: '{actual_date_column}' 컬럼 확인)")
             return pd.DataFrame()
        except Exception as e:
            logger.error(f"무신사 데이터 로드 중 예상치 못한 오류 발생: {e}", exc_info=True)
            return pd.DataFrame()
        finally:
            try:
                if cursor: cursor.close(); logger.debug("무신사 커서 닫힘")
                if conn and conn.is_connected(): conn.close(); logger.debug("무신사 DB 연결 닫힘(반환됨)")
            except Exception as e: logger.error(f"무신사 데이터 로드 finally 블록 오류: {e}")

# ==============================================================
# ==============================================================
# ==============================================================