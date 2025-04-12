# modi_search.py
import numpy as np
from typing import Dict, List, Any, Tuple, Union
import logging

# 로거 설정
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def calculate_cosine_similarity(vecs1: List[List[float]], vecs2: List[List[float]], top_k=10):
    """두 벡터 집합 간의 코사인 유사도 계산"""
    # 빈 벡터 리스트 체크
    if not vecs2:
        return [[] for _ in range(len(vecs1))]
    
    vecs2_arr = np.array(vecs2)
    vecs2_norm = np.linalg.norm(vecs2_arr, axis=1)
    
    results = []
    for vec1 in vecs1:
        vec = np.array(vec1)
        vec_norm = np.linalg.norm(vec)

        if vec_norm == 0:
            sim = np.zeros(len(vecs2))
        else:
            sim = np.dot(vecs2_arr, vec) / (vecs2_norm * vec_norm)        
        sim = np.nan_to_num(sim)

        # 결과 수가 top_k보다 적을 경우 처리
        top_k_actual = min(top_k, len(vecs2))
        if top_k_actual > 0:
            top_k_indices = np.argsort(sim)[-top_k_actual:][::-1]
            sim_top_k = [{'idx': i, 'sim_score': float(sim[i]), 'sim_vec': vecs2[i]} for i in top_k_indices]
        else:
            sim_top_k = []
        
        results.append(sim_top_k)
    
    return results

def search_similar_docs(keyword_vec: List[float], doc_vecs: Dict[int, List[float]], filtered_docs: List = None, top_k=5) -> List[int]:
    """
    키워드 벡터와 유사한 문서를 검색하여 반환
    
    Args:
        keyword_vec (List[float]): 검색 키워드 벡터
        doc_vecs (Dict[int, List[float]]): 문서 ID와 문서 벡터 사전
        filtered_docs (List, optional): 필터링된 문서 목록 (None이면 모든 문서 사용)
        top_k (int): 반환할 최대 문서 수
        
    Returns:
        List[int]: 문서 ID 목록 (항상 리스트 형태로 반환)
    """
    similar_docs = []  # 항상 리스트로 초기화
    
    try:
        # 키워드 벡터가 없거나 문서 벡터가 없으면 빈 리스트 반환
        if not keyword_vec or not doc_vecs:
            logger.warning("키워드 벡터 또는 문서 벡터가 없습니다.")
            return []

        # 키워드 벡터가 리스트가 아니면 빈 리스트 반환
        if not isinstance(keyword_vec, list):
            logger.warning(f"키워드 벡터가 리스트 타입이 아닙니다: {type(keyword_vec)}")
            return []
            
        # 필터링된 문서가 제공된 경우, 해당 문서들의 벡터만 사용
        filtered_doc_vecs = {}
        if filtered_docs and len(filtered_docs) > 0:
            for doc in filtered_docs:
                if hasattr(doc, '_doc_id') and doc._doc_id in doc_vecs:
                    filtered_doc_vecs[doc._doc_id] = doc_vecs[doc._doc_id]
        else:
            filtered_doc_vecs = doc_vecs
            
        # 필터링 후 문서 벡터가 없으면 빈 리스트 반환
        if not filtered_doc_vecs:
            logger.warning("필터링 후 사용 가능한 문서 벡터가 없습니다.")
            return []
            
        # 유사도 계산
        similarities = []
        for doc_id, doc_vec in filtered_doc_vecs.items():
            # 키워드 벡터와 문서 벡터의 차원이 같은지 확인
            if len(keyword_vec) != len(doc_vec):
                logger.debug(f"doc_id {doc_id}의 벡터 차원({len(doc_vec)})이 키워드 벡터 차원({len(keyword_vec)})과 다릅니다.")
                continue
                
            # 키워드 벡터와 문서 벡터가 모두 0이 아닌지 확인
            if np.linalg.norm(keyword_vec) == 0 or np.linalg.norm(doc_vec) == 0:
                logger.debug(f"doc_id {doc_id} 또는 키워드 벡터의 norm이 0입니다.")
                continue
                
            # 코사인 유사도 계산
            sim = np.dot(keyword_vec, doc_vec) / (np.linalg.norm(keyword_vec) * np.linalg.norm(doc_vec))
            similarities.append((doc_id, sim))
        
        # 유사도 기준으로 정렬
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 상위 K개 문서 ID 추출
        similar_docs = [doc_id for doc_id, _ in similarities[:top_k]]
        
        logger.info(f"유사 문서 {len(similar_docs)}개 발견")
        return similar_docs
            
    except Exception as e:
        logger.error(f"키워드 벡터 검색 오류: {e}", exc_info=True)
        return []  # 오류 발생 시 빈 리스트 반환

def retrieve_relevant_docs(doc_ids: List[int], fashion_datas: List, musinsa_datas: List) -> List[Dict]:
    """문서 ID 목록을 기반으로 실제 문서 데이터 반환"""
    relevant_docs = []
    
    # doc_ids가 빈 리스트면 빈 리스트 반환
    if not doc_ids:
        logger.warning("검색할 문서 ID가 없습니다.")
        return []
        
    # 문서 ID와 데이터 매핑
    for doc_id in doc_ids:
        # 패션 데이터에서 검색
        found = False
        if fashion_datas:
            for doc in fashion_datas:
                if hasattr(doc, '_doc_id') and doc._doc_id == doc_id:
                    doc_dict = {
                        "id": doc._doc_id,
                        "title": getattr(doc, '_title', "제목 없음"),
                        "content": getattr(doc, '_content', "내용 없음"),
                        "source": getattr(doc, '_source', "출처 없음"),
                        "type": "fashion"
                    }
                    relevant_docs.append(doc_dict)
                    logger.info(f"패션 문서 찾음: {doc_dict['title'][:30]}...")
                    found = True
                    break
                
        # 무신사 데이터에서도 검색
        if not found and musinsa_datas:
            for product in musinsa_datas:
                if hasattr(product, '_doc_id') and product._doc_id == doc_id:
                    product_dict = {
                        "id": product._doc_id,
                        "title": getattr(product, '_name', "제품명 없음"),
                        "content": f"브랜드: {getattr(product, '_brand', '정보 없음')}, 가격: {getattr(product, '_price', '정보 없음')}, 카테고리: {getattr(product, '_category', '정보 없음')}",
                        "source": "무신사",
                        "type": "musinsa"
                    }
                    relevant_docs.append(product_dict)
                    logger.info(f"무신사 상품 찾음: {product_dict['title'][:30]}...")
                    break
    
    logger.info(f"검색된 문서 수: {len(relevant_docs)}")
    return relevant_docs