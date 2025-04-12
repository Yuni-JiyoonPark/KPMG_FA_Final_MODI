import utils
from typing import Any, Dict, List, Set
from kiwipiepy import Kiwi


# 불용어 정의 (필요에 따라 확장 가능)
STOPWORDS = set([
    '있다', '하다', '되다', '등', '이', '그', '저', '것', '수', '더',
    '은', '는', '도', '으로', '들', '및', '의', '가', '에', '을', '를', '로', '과', '와',
    '한', '또한', '이번', '위한', '통해', '대한'
])


class ModiMorphAnalyze:
    def __init__(self):
        self._kiwi = Kiwi(num_workers=4, load_default_dict=True)
        print(f'ModiMorphAnalyze init kiwi complet.\n')
    

    # 형태소 분석 함수: 명사만 추출 + 불용어 제거 + 1글자 이상 (v0.8.0 호환)
    def extract_nouns(self, text: str):
        try:
            if text is None or len(text) == 0:
                return []
                
            # v0.8.0 방식으로 형태소 분석 수행
            tokens = self._kiwi.tokenize(text)
            
            # 명사만 추출 (NNG: 일반명사, NNP: 고유명사)
            nouns = []
            for token in tokens:
                word = token[0]  # 단어
                pos = token[1]   # 품사 태그
                
                # 명사이고 불용어가 아니며 2글자 이상인 경우만 추출
                if pos.startswith('NN') and word not in STOPWORDS and len(word) > 1:
                    nouns.append(word)
                    
            return nouns
        except Exception as e:
            print(f"### error ModiMorphAnalyze.extract_nouns() : {e}")
            return []