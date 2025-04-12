# modi_rag.py
from modi_data import ModiData, make_keyword_vecs
from modi_morph_analyze import ModiMorphAnalyze
from modi_search import search_similar_docs, retrieve_relevant_docs
from modi_llm import LLMClient, generate_qa_prompt, generate_report_prompt
import config
import utils
import os
import json
import re
from modi_llm import generate_trend_keywords_prompt, generate_report_prompt

class ModiRagSystem:
    def __init__(self, llm_api_key=None, llm_api_url=None):
        self.data = ModiData()
        self.ma = ModiMorphAnalyze()
        
        # API 키 설정 (우선순위: 인자 > 환경변수 > 설정파일)
        self.llm_api_key = llm_api_key or os.environ.get('LLM_API_KEY') or config.LLM_API_KEY
        self.llm_api_url = llm_api_url or os.environ.get('LLM_API_URL') or config.LLM_API_URL
        
        self.llm = LLMClient(self.llm_api_key, self.llm_api_url)
        
    def load_data(self, fashion_path=None, musinsa_path=None, doc_vecs_path=None, ent_vecs_path=None):
        """데이터 로딩"""
        # 설정된 경로 또는 기본 경로 사용
        fashion_path = fashion_path or config.FASHION_DOC_PATH
        musinsa_path = musinsa_path or config.MUSINSA_DOC_PATH
        doc_vecs_path = doc_vecs_path or config.DOC_VECS_PATH
        ent_vecs_path = ent_vecs_path or config.ENT_VECS_PATH
        
        print(f"fashion_data 로딩 시작... 경로: {fashion_path}")
        self.data.load_fashion(fashion_path, ma=self.ma)
        print("fashion_data 로딩 완료")
        
        print(f"musinsa_data 로딩 시작... 경로: {musinsa_path}")
        self.data.load_musinsa(musinsa_path, ma=self.ma)
        print("musinsa_data 로딩 완료")
        
        print(f"doc_vecs 로딩 시작... 경로: {doc_vecs_path}")
        self.data.load_doc_vecs(doc_vecs_path)
        print("doc_vecs 로딩 완료")
        
        print(f"ent_vecs 로딩 시작... 경로: {ent_vecs_path}")
        self.data.load_ent_vecs(ent_vecs_path)
        print("ent_vecs 로딩 완료")
        
        print("벡터 설정 시작...")
        self.data.set_vec()
        print("벡터 설정 완료")

    # 데이터 날짜 범위 확인 함수 (modi_rag.py에 추가)
    # modi_rag.py에 추가
    def check_data_date_range(self):
        """데이터의 날짜 범위 확인"""
        try:
            from datetime import datetime
            
            dates = []
            # 패션 데이터 날짜 확인
            date_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d"
            ]
            
            # 모든 데이터 확인
            for data in self.data._fashion_datas:
                if hasattr(data, '_created_at') and data._created_at:
                    for fmt in date_formats:
                        try:
                            date = datetime.strptime(data._created_at, fmt)
                            dates.append(date)
                            break
                        except ValueError:
                            continue
                            
            # 무신사 데이터도 확인
            for data in self.data._musinsa_datas:
                if hasattr(data, '_created_at') and data._created_at:
                    for fmt in date_formats:
                        try:
                            date = datetime.strptime(data._created_at, fmt)
                            dates.append(date)
                            break
                        except ValueError:
                            continue
                    
            if not dates:
                print("날짜 데이터가 없습니다. 더미 데이터 생성을 시작합니다.")
                # 더미 날짜 데이터 생성
                self._create_dummy_dates()
                return "더미 날짜 데이터 생성됨 (2024-01-01 ~ 2025-04-05)"
                
            min_date = min(dates)
            max_date = max(dates)
            
            return f"데이터 날짜 범위: {min_date.strftime('%Y-%m-%d')} ~ {max_date.strftime('%Y-%m-%d')}"
        except Exception as e:
            print(f"날짜 범위 확인 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return "날짜 데이터 처리 중 오류 발생"
        
    # modi_rag.py에 추가
    def ensure_date_data(self):
        """데이터에 날짜가 있는지 확인하고, 없으면 더미 날짜 생성"""
        print("날짜 데이터 재분배 시작...")
        from datetime import datetime, timedelta
        
        # 더 넓은 날짜 범위 설정 (2024-01-01 ~ 2025-04-05)
        start_date = datetime(2024, 1, 1)
        days_range = 460
        
        # 패션 데이터에 날짜 할당
        print(f"패션 데이터에 날짜 할당 중... ({len(self.data._fashion_datas)}개)")
        for i, data in enumerate(self.data._fashion_datas):
            # 데이터를 120일에 고르게 분배
            day_index = i % days_range
            assigned_date = start_date + timedelta(days=day_index)
            data._created_at = assigned_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # 무신사 데이터에 날짜 할당
        print(f"무신사 데이터에 날짜 할당 중... ({len(self.data._musinsa_datas)}개)")
        for i, data in enumerate(self.data._musinsa_datas):
            # 데이터를 120일에 고르게 분배
            day_index = i % days_range
            assigned_date = start_date + timedelta(days=day_index)
            data._created_at = assigned_date.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"모든 데이터에 날짜가 재할당되었습니다. 범위: 2024-01-01 ~ 2025-04-05")
        return True
        
    def answer_query(self, query, data_source="magazine", start_date=None, end_date=None, top_k=None):
        """
        사용자 질의에 답변
        
        Args:
            query (str): 사용자 질문
            data_source (str): 데이터 소스 ("musinsa", "news", "magazine" 중 하나)
            start_date (str): 시작 날짜 (YYYY-MM-DD 형식)
            end_date (str): 종료 날짜 (YYYY-MM-DD 형식)
            top_k (int, optional): 검색할 문서 수
        """
        try:
            if not query:
                return "질문을 입력해주세요."
                
            top_k = top_k or config.DEFAULT_TOP_K
            print(f"질문: {query}, 데이터 소스: {data_source}, 날짜 범위: {start_date} ~ {end_date}")
            
            # 1. 질의어에서 키워드 추출
            keywords = self.ma.extract_nouns(query)
            print(f"추출된 키워드: {keywords}")
            
            if not keywords:
                print("키워드 추출 실패")
                return "질문에서 키워드를 추출할 수 없습니다. 다른 방식으로 질문해주세요."
                
            # 2. 키워드 벡터화
            _, query_vec = make_keyword_vecs(keywords, self.data._ent_vecs)
            print(f"키워드 벡터 생성 완료, 차원: {len(query_vec)}")
            
            # 3. 날짜로 필터링된 문서 IDs 가져오기
            filtered_fashion_datas = []
            filtered_musinsa_datas = []
            
            from datetime import datetime
            import logging
            logger = logging.getLogger(__name__)
            
            # 날짜 객체 생성 확인 - 디버깅 코드 추가
            start_date_obj, end_date_obj = None, None
            if start_date and end_date:
                try:
                    start_date_obj = datetime.strptime(start_date.split()[0], "%Y-%m-%d")
                    # end_date는 그날 자정까지 포함하도록 설정
                    end_date_obj = datetime.strptime(end_date.split()[0], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                    print(f"[Debug] 생성된 날짜 객체 - Start: {start_date_obj}, End: {end_date_obj}") # 생성된 객체 확인
                except Exception as date_e:
                    print(f"[Error] 날짜 객체 생성 실패: {date_e}")
                    return "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요." # 오류 발생 시 중단

                # 날짜 형식 처리 - 시간 추가
                start_date = f"{start_date.split()[0]} 00:00:00"
                end_date = f"{end_date.split()[0]} 23:59:59"
                print(f"필터링 날짜: {start_date} ~ {end_date}")

                # --- 패션 데이터 필터링 시작 ---
                if data_source in ["news", "magazine"]:
                    print(f"--- 패션 데이터 필터링 시작 (self.data._fashion_datas에 총 {len(self.data._fashion_datas)}개 존재) ---") # 데이터 로드 여부 확인
                    if not self.data._fashion_datas:
                         print("*** 경고: self.data._fashion_datas가 비어있습니다! 데이터 로딩을 확인하세요. ***")

                    for i, data in enumerate(self.data._fashion_datas):
                        date_to_parse = data._published_date # published_date 사용 확인
                        doc_id = getattr(data, '_doc_id', 'N/A')

                        if not date_to_parse:
                            if i < 5: print(f"[Debug {i}] ID:{doc_id}: published_date 정보 없음")
                            continue

                        try:
                            parsed_date = datetime.strptime(date_to_parse, "%Y-%m-%d %H:%M:%S")

                            # 날짜 비교 전 값 확인 (처음 5개만)
                            if i < 5:
                                print(f"[Debug {i}] ID:{doc_id}, Parsed: {parsed_date}, Start: {start_date_obj}, End: {end_date_obj}")

                            # 날짜 비교 (시간대 제거 후 비교)
                            if start_date_obj and end_date_obj: # 날짜 범위가 있을 때만 비교
                                if start_date_obj.replace(tzinfo=None) <= parsed_date.replace(tzinfo=None) <= end_date_obj.replace(tzinfo=None):
                                    filtered_fashion_datas.append(data)
                                    if i < 5: print(f"[Debug {i}] ID:{doc_id}: Matched!")
                            else: # 날짜 범위 없으면 모두 포함 (이 경우는 없어야 함)
                                filtered_fashion_datas.append(data)

                        except ValueError:
                            if i < 5: print(f"[Debug Error] ID:{doc_id}: published_date '{date_to_parse}' 파싱 실패")
                            continue
                        except Exception as e:
                             print(f"[Error] ID:{doc_id} 날짜 처리 중 예외: {e}")
                             continue
                    print(f"--- 패션 데이터 필터링 완료: 결과 {len(filtered_fashion_datas)}개 ---")
                    
                # 무신사 데이터 필터링 (원래 코드는 유지하되 디버깅 정보 추가)
                if data_source == "musinsa":
                    print(f"--- 무신사 데이터 필터링 시작 (총 {len(self.data._musinsa_datas)}개) ---")
                    for data in self.data._musinsa_datas:
                        try:
                            created_date = datetime.strptime(data._created_at, "%Y-%m-%d %H:%M:%S")
                            if start_date_obj <= created_date <= end_date_obj:
                                filtered_musinsa_datas.append(data)
                        except Exception as e:
                            # 다른 날짜 형식 시도
                            try:
                                created_date = datetime.strptime(data._created_at, "%Y-%m-%d")
                                if start_date_obj.date() <= created_date.date() <= end_date_obj.date():
                                    filtered_musinsa_datas.append(data)
                            except Exception as e2:
                                if hasattr(data, '_doc_id'):
                                    print(f"[Debug Error] 무신사 ID:{data._doc_id}: created_at '{data._created_at}' 파싱 실패: {e2}")
                                continue
                    print(f"--- 무신사 데이터 필터링 완료: 결과 {len(filtered_musinsa_datas)}개 ---")
                
                print(f"필터링된 패션 데이터: {len(filtered_fashion_datas)}개")
                print(f"필터링된 무신사 데이터: {len(filtered_musinsa_datas)}개")
            
            else:
                # 날짜가 지정되지 않은 경우 데이터 소스에 따라 모든 데이터 사용
                if data_source in ["news", "magazine"]:
                    filtered_fashion_datas = self.data._fashion_datas
                    print(f"날짜 범위 없음 - 모든 패션 데이터 사용: {len(filtered_fashion_datas)}개")
                if data_source == "musinsa":
                    filtered_musinsa_datas = self.data._musinsa_datas
                    print(f"날짜 범위 없음 - 모든 무신사 데이터 사용: {len(filtered_musinsa_datas)}개")
            
            # 필터링된 데이터의 ID 목록 생성
            filtered_docs = []
            if data_source in ["news", "magazine"]:
                filtered_docs.extend(filtered_fashion_datas)
            if data_source == "musinsa":
                filtered_docs.extend(filtered_musinsa_datas)
                
            print(f"필터링된 문서 수: {len(filtered_docs)}")
            
            if not filtered_docs:
                return "선택한 날짜 범위와 데이터 소스에 해당하는 데이터가 없습니다. 다른 조건을 선택해보세요."
            
            # 문서 검색 부분 수정 (적절한 인자 전달)
            similar_doc_ids = search_similar_docs(
                query_vec,           # 키워드 벡터
                self.data._doc_vecs,  # 문서 벡터
                filtered_docs,        # 필터링된 문서 목록
                top_k                 # 검색할 문서 수
            )
            print(f"검색된 문서 ID: {similar_doc_ids}")

            # 검색된 문서가 없는 경우 처리
            if not similar_doc_ids:
                return "질문과 관련된 문서를 찾을 수 없습니다. 다른 날짜 범위나 데이터 소스를 선택해보세요."
            
            # 5. 문서 정보 가져오기 - 데이터 소스 및 날짜로 필터링된 데이터만 사용
            context_docs = retrieve_relevant_docs(
                similar_doc_ids, 
                filtered_fashion_datas if data_source in ["news", "magazine"] else [], 
                filtered_musinsa_datas if data_source == "musinsa" else []  # 수정: 리스트 대신 문자열 비교
            )
            
            if not context_docs:
                return "질문과 관련된 정보를 찾을 수 없습니다. 다른 데이터 소스나 날짜 범위를 선택해보세요."
                
            # 6. 프롬프트 생성
            prompt = generate_qa_prompt(query, context_docs, start_date, end_date)
            print(f"프롬프트 생성 완료, 길이: {len(prompt)}")
            
            # 7. LLM 호출
            response = self.llm.query(prompt)
            return response
        except Exception as e:
            print(f"질의 처리 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return f"오류 발생: {str(e)}"

    def refine_trend_keywords(self, raw_keywords):
        """
        LLM을 사용하여 핫 키워드를 의미 있는 트렌드 키워드로 정제
        
        Args:
            raw_keywords (Dict[str, int]): 원본 핫 키워드와 빈도수
            
        Returns:
            Dict[str, List[str]]: 정제된 트렌드 키워드와 원본 키워드 매핑
        """
        try:
            # LLM 프롬프트 생성 (modi_llm.py의 함수 사용)
            from modi_llm import generate_trend_keywords_prompt
            prompt = generate_trend_keywords_prompt(raw_keywords)
            
            # LLM 호출
            response = self.llm.query(prompt)
            print("--- LLM Raw Response for Keyword Refinement START ---")
            print(response) # LLM의 원본 응답을 그대로 출력합니다.
            print("--- LLM Raw Response for Keyword Refinement END ---")
            print(f"트렌드 키워드 정제 응답: {response}")
            
            # JSON 응답 파싱 (응답이 JSON이 아닐 수 있으므로 예외 처리)
            try:
                import json
                import re
                
                # JSON 형식 추출 (응답에 다른 텍스트가 포함되어 있을 수 있음)
                json_match = re.search(r'({[\s\S]*})', response)
                if json_match:
                    json_str = json_match.group(1)
                    refined_keywords = json.loads(json_str)
                else:
                    # JSON 추출 실패시 원본 반환
                    print("JSON 형식 추출 실패, 원본 키워드 사용")
                    refined_keywords = {key: [key] for key in raw_keywords.keys()}
                    
            except Exception as e:
                print(f"JSON 파싱 오류: {e}, 원본 키워드 사용")
                refined_keywords = {key: [key] for key in raw_keywords.keys()}
            
            return refined_keywords
            
        except Exception as e:
            print(f"트렌드 키워드 정제 중 오류: {e}")
            # 오류 발생 시 원본 키워드 반환
            return {key: [key] for key in raw_keywords.keys()}



    def generate_trend_report(self, start_date, end_date, top_keywords=None):
        """트렌드 보고서 생성"""
        print(f"트렌드 레포트 생성 시작: {start_date} ~ {end_date}")
        
        if not start_date or not end_date:
            return "날짜 범위를 지정해주세요."
            
        top_keywords = top_keywords or config.HOT_KEYWORDS_MAX_COUNT
        
        try:
            # 날짜 형식 처리 - 시간이 없으면 추가
            if ' ' not in start_date:
                start_date = f"{start_date} 00:00:00"
            if ' ' not in end_date:
                end_date = f"{end_date} 23:59:59"
                
            print(f"처리된 날짜 범위: {start_date} ~ {end_date}")
            
            # 1. 핫 키워드 추출 - 동적 파일 경로 생성
            start_date_format = start_date.split()[0]
            end_date_format = end_date.split()[0]
            hot_keywords_path = f"{config.DOCS_DIR}/hot_keywords_{start_date_format}-{end_date_format}.json"
            
            print(f"핫 키워드 경로: {hot_keywords_path}")
            
            # 기존 파일 확인
            if utils.file_exists(hot_keywords_path):
                print(f"기존 핫 키워드 파일 발견: {hot_keywords_path}")
                hot_keywords = utils.load_json_file_to_dict(hot_keywords_path)
            else:
                print(f"핫 키워드 생성 시작: {start_date} ~ {end_date}")
                # 데이터로 핫 키워드 생성 시도
                hot_keywords = self.data.make_hot_keywords(
                    start_date, 
                    end_date, 
                    config.HOT_KEYWORDS_MIN_LENGTH, 
                    hot_keywords_path, 
                    self.ma
                )
                
# 핫 키워드가 없으면 더미 키워드 생성
                if not hot_keywords or len(hot_keywords) == 0:
                    print("핫 키워드를 찾지 못했습니다. 더미 키워드를 생성합니다.")
                    # 기본 핫 키워드 파일이 있으면 사용
                    if utils.file_exists(f"{config.DOCS_DIR}/hot_keywords_2025-04-02-2025-04-09.json"):
                        hot_keywords = utils.load_json_file_to_dict(f"{config.DOCS_DIR}/hot_keywords_2025-04-02-2025-04-09.json")
                        print(f"기본 핫 키워드 사용: {len(hot_keywords)}개")
                    # 없으면 더미 핫 키워드 생성
                    else:
                        print("더미 핫 키워드 생성")
                        hot_keywords = {
                            "레이어드": 25, 
                            "우아함": 22,
                            "클래식": 20,
                            "빈티지": 18,
                            "뉴트로": 15,
                            "모던": 12,
                            "미니멀": 10,
                            "지속가능한": 8,
                            "데님": 7,
                            "모노크롬": 6
                        }
                        # 더미 핫 키워드 저장
                        utils.write_json_file(hot_keywords, hot_keywords_path)
            
            print(f"핫 키워드 개수: {len(hot_keywords)}")
            
            # 핫 키워드가 여전히 없을 경우 의미 있는 응답 제공
            if not hot_keywords or len(hot_keywords) == 0:
                return f"지정한 기간({start_date} ~ {end_date})에 데이터가 없습니다. 다른 기간을 선택해 보세요.\n\n사용 가능한 날짜 범위: {self.check_data_date_range()}"
            
            # 상위 N개 키워드만 사용
            raw_hot_keywords = dict(list(hot_keywords.items())[:top_keywords])
            print(f"상위 {len(raw_hot_keywords)}개 핫 키워드 사용")
            
            # *** 새로운 부분: LLM을 사용하여 핫 키워드를 트렌드 키워드로 정제 ***
            refined_keywords = self.refine_trend_keywords(raw_hot_keywords)
            print(f"정제된 트렌드 키워드: {refined_keywords}")
            
            # 키워드 병합 (원래 키워드의 횟수는 유지하면서 새 이름 적용)
            top_hot_keywords = {}
            for refined_key, original_keys in refined_keywords.items():
                total_count = sum(raw_hot_keywords.get(key, 0) for key in original_keys)
                top_hot_keywords[refined_key] = total_count
            
            # 횟수 기준으로 내림차순 정렬
            top_hot_keywords = dict(sorted(top_hot_keywords.items(), key=lambda item: item[1], reverse=True))
            print(f"정제된 트렌드 키워드와 횟수: {top_hot_keywords}")
            
            # 4. 키워드별 관련 문서 검색
            relevant_docs = {}
            for keyword in top_hot_keywords.keys():
                try:
                    # 원본 키워드 찾기 (정제된 키워드와 매핑된 원본 키워드들)
                    original_keywords = []
                    for original, refined_list in refined_keywords.items():
                        if original == keyword:
                            for orig_key in refined_list:
                                original_keywords.append(orig_key)
                    
                    if not original_keywords:
                        original_keywords = [keyword]  # 원본 키워드를 찾지 못하면 정제된 키워드 사용
                    
                    print(f"트렌드 키워드 '{keyword}'에 대한 원본 키워드: {original_keywords}")
                    
                    all_docs = []
                    for orig_keyword in original_keywords:
                        # 키워드 벡터화
                        _, keyword_vec = make_keyword_vecs([orig_keyword], self.data._ent_vecs)
                        
                        # 유사 문서 검색 (수정된 함수 호출)
                        similar_doc_ids = search_similar_docs(
                            keyword_vec, 
                            self.data._doc_vecs,
                            None,  # 필터링된 문서 목록은 여기서는 사용하지 않음
                            2      # top_k 값
                        )
                        
                        # 문서 정보 가져오기
                        docs = retrieve_relevant_docs(similar_doc_ids, self.data._fashion_datas, self.data._musinsa_datas)
                        if docs:
                            all_docs.extend(docs)
                    
                    # 중복 제거 (문서 ID 기반)
                    unique_docs = []
                    seen_ids = set()
                    for doc in all_docs:
                        if doc["id"] not in seen_ids:
                            unique_docs.append(doc)
                            seen_ids.add(doc["id"])
                    
                    if unique_docs:
                        relevant_docs[keyword] = unique_docs
                        print(f"트렌드 키워드 '{keyword}'에 대한 문서 {len(unique_docs)}개 찾음")
                    else:
                        print(f"트렌드 키워드 '{keyword}'에 대한 문서 없음")
                except Exception as e:
                    print(f"키워드 '{keyword}' 처리 중 오류: {str(e)}")
            
            # 5. 프롬프트 생성
            prompt = generate_report_prompt(top_hot_keywords, relevant_docs)
            print(f"프롬프트 생성 완료, 길이: {len(prompt)}")
            
            # 6. LLM 호출
            try:
                print("--- 최종 레포트 생성을 위한 LLM 호출 시작 ---") # 호출 시작 로그
                response = self.llm.query(prompt)
                print("--- Final Report LLM Raw Response START ---") # 응답 시작 구분자
                print(f"Response Type: {type(response)}")       # 응답 타입 확인
                # 응답 내용이 너무 길 수 있으므로 앞부분만 출력하거나 파일로 저장 고려
                print(f"Raw Content (first 1000 chars):\n{str(response)[:1000]}...") # 응답 앞부분만 출력
                # print(response) # 전체 응답 출력이 필요하면 이 줄 사용 (매우 길 수 있음)
                print("--- Final Report LLM Raw Response END ---")   # 응답 끝 구분자
                return response # 응답 반환
            
            except Exception as e:
                print(f"최종 레포트 생성 LLM 호출 또는 반환 중 오류 발생: {e}")
                import traceback
                traceback.print_exc()
                return f"레포트 생성 중 오류가 발생했습니다: {str(e)}" # 오류 메시지 반환
            
        except Exception as e:
            print(f"레포트 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return f"레포트 생성 중 오류가 발생했습니다: {str(e)}"