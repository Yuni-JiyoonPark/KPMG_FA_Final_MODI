
![modi-logo](https://github.com/your-org/modi/assets/your-logo.png)

> 빠르게 변화하는 패션 시장에서, 바잉 MD들은 반복적인 서류 업무와 트렌드 조사로 인해 전략적 의사결정에 집중하기 어려운 환경에 처해 있습니다.  
> MODI는 이러한 문제를 해결하기 위해 만들어진 **AI 기반 실무형 업무 자동화 솔루션**입니다.  
> OCR + Vector Search + 생성형 모델 기술을 활용해 문서 기반의 일정을 자동 추출하고, 글로벌 트렌드 분석을 자동화함으로써  
> **패션 MD들이 더 전략적인 업무에 집중할 수 있도록 지원합니다.**

---

## 👥 Team Members

| [<img src="https://avatars.githubusercontent.com/u/00000001?v=4" width="130"/>](#) | [<img src="https://avatars.githubusercontent.com/u/00000002?v=4" width="130"/>](#) | [<img src="https://avatars.githubusercontent.com/u/00000003?v=4" width="130"/>](#) | [<img src="https://avatars.githubusercontent.com/u/00000004?v=4" width="130"/>](#) |
| :--: | :--: | :--: | :--: |
| **박정훈**<br>`PL · DBA · FE`<br>🧠 시스템 통합 / DB / 프론트 일부 | **지연주**<br>`PM · DS · TR`<br>📋 기획 / 데이터 분석 / 트렌드 리서치 | **박지윤**<br>`PM · DS · TR`<br>📊 기획 보조 / 분석 / 트렌드 리서치 | **서누리**<br>`BE · FE · UX · OCR`<br>💻 백엔드 / 프론트 / UX / OCR |
| [![GitHub](https://img.shields.io/badge/GitHub-Link-181717?logo=github)](https://github.com/junghoon) | [![GitHub](https://img.shields.io/badge/GitHub-Link-181717?logo=github)](https://github.com/yeonju) | [![GitHub](https://img.shields.io/badge/GitHub-Link-181717?logo=github)](https://github.com/jiyoon) | [![GitHub](https://img.shields.io/badge/GitHub-Link-181717?logo=github)](https://github.com/nuri) |

---

## 🧭 프로젝트 개요

### 🎯 프로젝트명
**PROJECT MODI**

### 📝 목표
- 반복 작업을 자동화하고, **패션 MD의 전략적 의사결정**을 지원하는 AI 기반 솔루션 구축

### 🧩 주요 기능
- 📄 **OCR 기반 일정 추출 및 비교**
- 📊 **트렌드 분석 자동화**
- 🔍 **RAG 기반 문서 검색 + GPT-4o-mini 요약**
- 🗓 **일정 대시보드 + 자동 리포트 생성**

---

## 💡 기술 스택

### 🎨 Frontend
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

### ⚙️ Backend
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2-black?logo=flask&logoColor=white)

### 🤖 AI & Search
![TF-IDF](https://img.shields.io/badge/TF--IDF-분석-FFD700)
![NetworkX](https://img.shields.io/badge/NetworkX-연관어분석-6495ED)
![RAG](https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-F57C00)
![GPT-4o-mini](https://img.shields.io/badge/GPT--4o--mini-LLM-blueviolet?logo=openai)

### 👁️ OCR
![Google Vision](https://img.shields.io/badge/Google_Vision_API-OCR-F44336?logo=googlecloud)

### 🗃️ Database
![MySQL](https://img.shields.io/badge/MySQL-Relational_DB-4479A1?logo=mysql&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-008080?logo=qdrant)

---

## 📌 주요 기능 요약

| 기능 | 설명 |
|------|------|
| 🧾 **문서 기반 일정 자동 추출** | OCR을 통해 Order/Invoice에서 날짜, 항목, 수량 등 핵심 정보 자동화 |
| 🔍 **임베딩 기반 검색기** | 사용자 질의에 대해 유사 문서 자동 탐색 및 요약 (RAG + GPT-4o-mini) |
| 📊 **트렌드 분석 대시보드** | 매거진 및 무신사 데이터를 기반으로 자동 분석 시각화 |
| 🧮 **항목 비교 자동화** | 주문서 vs 인보이스 비교 및 불일치 자동 하이라이팅 |
| 🗓 **일정 대시보드 및 우선순위 관리** | 개인화 기반 일정 자동 갱신 및 주요 일정 알림 |

---

## 🎯 기대 효과

- ✅ **문서 자동추출 편의성**: 평균 4.25점
- ✅ **업무 전략성 향상**: 전략적 판단 지원, 실시간 일정 관리
- ✅ **트렌드 대응력 강화**: TF-IDF 기반 요약 및 시각화
- ✅ **개인화 대시보드**: 사용자별 우선순위 중심 정보 구조 제공
- ✅ **타 경쟁사 대비 자동화 수준 우위**: 비교/검색/요약/캘린더까지 E2E 지원

---

## 🧭 시스템 아키텍처

```plaintext
User
 └─ Upload Document (PDF/JPG)
     ├─ OCR → Google Vision
     ├─ Tokenization + Embedding → Qdrant
     ├─ Query → Similar Documents Search (RAG)
     └─ GPT-4o-mini Summary → Dashboard
                          └─ Keyword Visualization / Trend Report
```
