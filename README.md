# PROJECT MODI
> 패션 MD 업무 효율화를 위한 AI 기반 실무형 솔루션

final_card_readme = """
![modi-logo](https://github.com/KpmgFuture-Academy/fa02_fin_MODI/blob/main/img/modi_logo.png)

> 빠르게 변화하는 패션 시장에서, 바잉 MD들은 반복적인 서류 업무와 트렌드 조사로 인해 전략적 의사결정에 집중하기 어려운 환경에 처해 있습니다.  
> MODI는 이러한 문제를 해결하기 위해 만들어진 **AI 기반 실무형 업무 자동화 솔루션**입니다.  
> OCR + NLP + Vector Search 기술을 활용해 문서 기반의 일정을 자동 추출하고, 글로벌 트렌드 분석을 자동화함으로써  
> **패션 MD들이 더 전략적인 업무에 집중할 수 있도록 지원합니다.**

---

## 👥 Team Members

| <img src="https://github.com/KpmgFuture-Academy/fa02_fin_MODI/blob/main/img/jh.png" width="130"/> | <img src="https://github.com/KpmgFuture-Academy/fa02_fin_MODI/blob/main/img/yj.png" width="130"/> | <img src="https://github.com/KpmgFuture-Academy/fa02_fin_MODI/blob/main/img/jy.png" width="130"/> | <img src="https://github.com/KpmgFuture-Academy/fa02_fin_MODI/blob/main/img/nr.png" width="130"/> |
|:--:|:--:|:--:|:--:|
| **박정훈**<br>PL · DBA · FE<br>🧠 시스템 통합 / DB / 프론트 일부<br>[![GitHub](https://img.shields.io/badge/GitHub-junghoon-181717?logo=github)](https://github.com/junghoon) | **지연주**<br>PM · DA · TR<br>📋 기획 / 데이터 분석 및 수집 / 트렌드 리서치<br>[![GitHub](https://img.shields.io/badge/GitHub-yeonju-181717?logo=github)](https://github.com/yeonju) | **박지윤**<br>PM · DA · TR<br>📊 기획 / 데이터 분석 및 수집 / 트렌드 리서치<br>[![GitHub](https://img.shields.io/badge/GitHub-jiyoon-181717?logo=github)](https://github.com/jiyoon) | **서누리**<br>BE · FE · UX · OCR<br>💻 백엔드 / 프론트 / UX / OCR<br>[![GitHub](https://img.shields.io/badge/GitHub-nuri-181717?logo=github)](https://github.com/nuri) |

| 이름            | 역할 요약 |
|-----------------|--------------------------------------------------------|
| **박정훈** (PL, DBA, FE)       | 🧠 Team Lead, DB 설계 및 관리, 프론트 일부 구현, 시스템 통합, Vector DB 설계 |
| **지연주** (PM, DS, TR)        | 📋 프로젝트 총괄 기획, 데이터 분석 및 수집, 트렌드 리서치 |
| **박지윤** (PM, DS, TR)        | 📊 프로젝트 기획 및 데이터 분석 및 수집, 데이터 전처리, 트렌드 분석 |
| **서누리** (BE, FE, UX, OCR)  | 💻 백엔드 개발, 프론트 구현, UX 설계 및 화면 구성, OCR 개발 |

### 🗂 역할 약어 설명

| 약어 | 설명                       |
|------|----------------------------|
| PL   | Project Leader             |
| PM   | Project Manager            |
| FE   | Frontend Engineer          |
| BE   | Backend Engineer           |
| DA   | Data Analyst               |
| DBA  | Database Administrator     |
| UX   | User Experience Designer   |
| TR   | Trend Analyst              |

---

## 🛠 기술 스택

### 📊 데이터 및 분석

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Kiwi 형태소 분석기](https://img.shields.io/badge/Kiwi-Tokenize-FFB6C1?logoColor=white)
![TF-IDF](https://img.shields.io/badge/TF--IDF-분석-FFD700)
![NetworkX](https://img.shields.io/badge/NetworkX-그래프분석-6495ED)
![GPT-4o-mini](https://img.shields.io/badge/LLM-GPT--4o--mini-blueviolet?logo=openai)

### 🧠 AI & OCR

![Google Cloud Vision API](https://img.shields.io/badge/Google_Vision_OCR-F44336?logo=googlecloud&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-검색_기반_생성-F57C00?logo=openai&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-벡터DB-008080?logo=qdrant)

### 💻 백엔드

![Flask](https://img.shields.io/badge/Flask-2.2-black?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Relational_DB-4479A1?logo=mysql&logoColor=white)

### 📊 프론트엔드

![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

---

## 📌 주요 기능 요약

| 기능 | 설명 |
|------|------|
| 🧾 **문서 기반 일정 자동 추출** | OCR을 통해 Order/Invoice에서 날짜, 항목, 수량 등 핵심 정보 자동화 |
| 📊 **트렌드 분석 대시보드** | Vogue, WWD, W Korea 등 매거진 기반 트렌드 자동 분석 (TF-IDF / 네트워크 분석) |
| 🔎 **임베딩 기반 검색기** | 사용자 질의에 대해 유사 문서 자동 탐색 및 요약 (RAG 기반) |
| 🧠 **자동화 리포트 생성기** | 뉴스/상품 데이터 기반 트렌드 리포트를 자연어로 생성 |
| 🧮 **항목별 자동 비교기** | 주문서 vs 인보이스 비교 및 불일치 자동 하이라이팅 표시 |

---

## 🎯 핵심 성과

- 평균 응답 점수 4.2 / 5.0  
- 사용자 100% 긍정 응답: "정보 탐색 속도 향상", "문서 자동처리 만족"
- 전략적 업무 비중 증가 → 반복 작업 최소화

---

## 🧭 시스템 아키텍처

```plaintext
유저
 └─ 업로드 (문서 / 키워드)
     ├─ [OCR] Google Vision API → 핵심 항목 추출
     ├─ [Embedding] 형태소 분석 + 벡터 저장 (Qdrant / MySQL)
     └─ [검색 & 요약] RAG + GPT-4o-mini 기반 답변 생성
           └─ 대시보드로 시각화 및 리포트 제공
