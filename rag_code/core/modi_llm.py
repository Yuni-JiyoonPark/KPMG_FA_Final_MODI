# modi_llm.py
import requests
import json
import os
from typing import Dict, List, Any

class LLMClient:
    def __init__(self, api_key: str = None, api_url: str = None):
        # 환경 변수 또는 인자로 받은 값 활용
        self.api_key = api_key or os.environ.get('LLM_API_KEY')
        self.api_url = api_url or os.environ.get('LLM_API_URL', 'https://api.openai.com/v1/chat/completions')
        
        if not self.api_key:
            print("경고: API 키가 제공되지 않았습니다. LLM 호출이 실패할 수 있습니다.")
            
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
    
    def query(self, prompt: str, max_retries: int = 3) -> str:
        """LLM API 호출"""
        if not self.api_key:
            raise ValueError("API 키가 설정되지 않았습니다.")
            
        payload = {
            "model": "gpt-4o-mini",  # 또는 다른 모델
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        retries = 0
        while retries < max_retries:
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=30  # 타임아웃 설정
                )
                
                if response.status_code == 200:
                    response_json = response.json()
                    # 응답 형식 검증
                    if "choices" in response_json and len(response_json["choices"]) > 0:
                        return response_json["choices"][0]["message"]["content"]
                    else:
                        raise ValueError(f"응답 형식이 예상과 다릅니다: {response_json}")
                else:
                    print(f"API 호출 실패 (시도 {retries+1}/{max_retries}): {response.status_code}")
                    if retries + 1 >= max_retries:
                        raise Exception(f"API 호출 실패: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"네트워크 오류 (시도 {retries+1}/{max_retries}): {e}")
                if retries + 1 >= max_retries:
                    raise
            
            retries += 1
        
        raise Exception("최대 재시도 횟수 초과")
    
def generate_qa_prompt(query: str, context_docs: List[Dict], start_date=None, end_date=None) -> str:
    """질답 시스템용 프롬프트 생성"""
    prompt = f"다음 정보를 바탕으로 질문에 답변해주세요. 정보에 없는 내용은 '관련 정보가 없습니다'라고 답변하세요.\n\n"
    
    # 날짜 범위 정보 추가
    if start_date and end_date:
        prompt += f"### 날짜 범위: {start_date.split()[0]} ~ {end_date.split()[0]}\n\n"
    
    prompt += "### 정보:\n"
    for i, doc in enumerate(context_docs, 1):
        # 필드 존재 여부 확인
        title = doc.get('title', '제목 없음')
        content = doc.get('content', '내용 없음')
        doc_type = doc.get('type', '불명')
        
        prompt += f"{i}. [{doc_type}] {title}\n"
        prompt += f"   내용: {content[:300]}...\n\n"
    
    prompt += f"### 질문: {query}\n\n"
    prompt += "### 답변:"
    
    return prompt


def generate_report_prompt(hot_keywords: Dict[str, int], relevant_docs: Dict[str, List[Dict]]) -> str:
    """GPT 프롬프트 엔지니어링 기법 적용된 트렌드 보고서 생성용 프롬프트"""
    
    # 프롬프트 서두: Role Prompting
    prompt = (
        "당신은 Z세대 중심 커머스 플랫폼에서 근무하는 전문 바잉 MD AI입니다.\n"
        "뉴스, 패션 매거진, 커머스 데이터를 기반으로 트렌드 인사이트 리포트를 작성해주세요.\n"
        "이 리포트는 바잉 전략 및 마케팅 실행에 바로 활용될 수 있어야 하며, "
        "트렌드 탐지 → 분석 → 전략 제안 흐름을 따라야 합니다.\n\n"
    )
    
    # 키워드 소개 (Few-shot Prompting 스타일)
    prompt += "### 📌 인기 키워드 (언급량 기준):\n"
    for keyword, count in hot_keywords.items():
        prompt += f"- {keyword} ({count}회 언급)\n"
    
    # 관련 문서 요약
    prompt += "\n### 📰 관련 정보 요약:\n"
    for keyword, docs in relevant_docs.items():
        if docs:
            prompt += f"\n#### 🔍 키워드: {keyword}\n"
            for i, doc in enumerate(docs[:3], 1):
                prompt += f"{i}. 제목: {doc['title']}\n"
                prompt += f"   내용 요약: {doc['content'][:200].strip()}...\n"
    
    # 분석 지시사항 (Chain-of-Thought + Self-Ask 통합)
    prompt += (
        "\n### 🧠 리포트 작성 지시사항:\n"
        "아래 항목에 따라 데이터를 기반으로 분석 보고서를 작성하세요. "
        "모든 항목은 숫자/키워드 기반 근거를 포함하고, 명확하게 구분하여 작성하세요.\n\n"
        
        "1. [트렌드 키워드 및 설명]\n"
        "- 1~3개 핵심 트렌드 키워드 요약 및 간단한 설명 작성\n\n"
        
        "2. [연관 아이템 분석]\n"
        "- 해당 키워드에 관련된 인기 브랜드/상품/가격대를 정리하세요\n\n"
        
        "3. [부상 배경 분석]\n"
        "- 다음 질문을 차례대로 고려해 설명하세요:\n"
        "  ① 이 트렌드는 어떤 사회/문화/경제 변화와 관련되었나요?\n"
        "  ② 어떤 소비자 심리나 니즈와 맞물려 있나요?\n"
        "  ③ 처음 어디서 확산되었나요 (SNS, 브랜드 등)?\n\n"
        
        "4. [매거진별 트렌드 요약]\n"
        "- 각 매거진 별(source 별로)에서 해당 키워드를 어떻게 다루고 있는지 1~2문장으로 요약하세요\n\n"
        
        "5. [이커머스 반영 현황]\n"
        "- 무신사 상품/리뷰 데이터를 기반으로 해당 트렌드가 반영된 예시를 분석하세요\n\n"
        
        "6. [계절성 분석]\n"
        "- 전년도 동 시즌 데이터와 비교하여 계절성 패턴이 있는지 판단하세요\n\n"
        
        "7. [트렌드 생애주기 분석]\n"
        "- 다음 질문에 답하며 도입/성장/성숙/쇠퇴기 여부를 판단하세요:\n"
        "  ① 키워드가 처음 등장한 시점은?\n"
        "  ② 최근 노출/언급/리뷰 수는 증가 중인가요?\n"
        "  → 지속 유행 or 반짝 유행 여부 판단\n\n"
        
        "8. [바잉 MD 전략 제안]\n"
        "- 당신은 Z세대 타겟 바잉 MD입니다. 아래 전략을 제시하세요:\n"
        "  ✅ 어떤 브랜드/아이템에 집중할 것인가\n"
        "  ✅ 어떤 시즌/채널/메시지로 마케팅할 것인가\n"
        "  ✅ 기획전/배너/프로모션 전략\n\n"
    )
    
    # 출력 형식 제안
    prompt += (
        "📌 리포트는 Markdown 형식 또는 JSON 형식 중 하나로 명확하게 작성하세요.\n"
        "분석 항목마다 제목을 구분하고, 중복 없이 간결하고 실용적으로 작성하세요."
    )
    
    return prompt

def generate_trend_keywords_prompt(raw_keywords: Dict[str, int]) -> str:
    """트렌드 키워드 정제를 위한 프롬프트 생성"""
    
    # 키워드를 문자열로 변환
    keywords_text = ", ".join([f"{key}({count})" for key, count in raw_keywords.items()])
    
    prompt = f"""
당신은 패션 트렌드 분석 전문가입니다. 다음 키워드들을 분석해서 5-7개의 고급스러운 패션 트렌드 키워드로 재구성해주세요.

### 현재 키워드 목록 (빈도수 포함):
{keywords_text}

### 작업 지침:
1. 유사하거나 관련된 키워드들을 그룹화하세요
2. 각 그룹에 세련된 패션 트렌드 명칭을 붙여주세요 (예: "Layered Elegance", "Neo-Bourgeois" 등)
3. 명칭은 영어 또는 한국어로 표현해도 좋습니다
4. 트렌드 명칭은 패션 매거진에 어울리는 세련된 표현이어야 합니다
5. 원래 키워드와 너무 동떨어진 표현은 피해주세요

### 응답 형식:
{{
  "트렌드 키워드 1": ["원본 키워드 1", "원본 키워드 2", ...],
  "트렌드 키워드 2": ["원본 키워드 3", "원본 키워드 4", ...],
  ...
}}

위 형식의 JSON 객체만 반환해주세요.
"""
    
    return prompt