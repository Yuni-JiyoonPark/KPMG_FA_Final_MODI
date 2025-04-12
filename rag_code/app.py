import os
from flask import Flask, render_template, request, jsonify
from modi_rag import ModiRagSystem
import config

# Flask 앱 초기화
app = Flask(__name__)

# 디버깅 모드 설정
app.debug = True

# RAG 시스템 초기화
try:
    print("RAG 시스템 초기화 시작...")
    rag_system = ModiRagSystem()
    print("ModiRagSystem 인스턴스 생성 완료")
    
    # 데이터 로딩
    print("fashion_data 로딩 시작...")
    rag_system.data.load_fashion(config.FASHION_DOC_PATH)
    print("fashion_data 로딩 완료")
    
    print("musinsa_data 로딩 시작...")
    rag_system.data.load_musinsa(config.MUSINSA_DOC_PATH)
    print("musinsa_data 로딩 완료")
    
    print("doc_vecs 로딩 시작...")
    rag_system.data.load_doc_vecs(config.DOC_VECS_PATH)
    print("doc_vecs 로딩 완료")
    
    print("ent_vecs 로딩 시작...")
    rag_system.data.load_ent_vecs(config.ENT_VECS_PATH)
    print("ent_vecs 로딩 완료")
    
    # RAG 시스템 초기화 부분에 추가
    print("날짜 데이터 확인 시작...")
    rag_system.ensure_date_data()
    print("날짜 데이터 확인 완료")

    print("벡터 설정 시작...")
    rag_system.data.set_vec()
    print("벡터 설정 완료")
    
    rag_system_initialized = True
    print("RAG 시스템 초기화 완료!")
except Exception as e:
    print(f"RAG 시스템 초기화 중 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()
    rag_system_initialized = False
    rag_system = None

# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data-info')
def data_info():
    if not rag_system_initialized:
        return jsonify({"info": "RAG 시스템이 초기화되지 않았습니다."})
    
    date_range = rag_system.check_data_date_range()
    return jsonify({"info": date_range})

# 질문 처리 API
@app.route('/api/ask', methods=['POST'])
def ask_question():
    if not rag_system_initialized:
        return jsonify({"response": "RAG 시스템이 초기화되지 않았습니다. 관리자에게 문의하세요."}), 500
    
    try:
        data = request.json
        query = data.get("query", "")
        data_source = data.get("data_source", "magazine")  # 기본값을 magazine으로 변경
        start_date = data.get("start_date", None)  # 날짜 범위 파라미터 추가
        end_date = data.get("end_date", None)  # 날짜 범위 파라미터 추가
        
        response = rag_system.answer_query(query, data_source, start_date, end_date)
        return jsonify({"response": response})
    except Exception as e:
        print(f"질문 처리 중 오류: {e}")
        return jsonify({"response": f"오류 발생: {str(e)}"}), 500
    
# 레포트 생성 API
@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    if not rag_system_initialized:
        return jsonify({"report": "RAG 시스템이 초기화되지 않았습니다. 관리자에게 문의하세요."}), 500
    
    try:
        data = request.json
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        report = rag_system.generate_trend_report(start_date, end_date)
        return jsonify({"report": report})
    except Exception as e:
        print(f"레포트 생성 중 오류: {e}")
        return jsonify({"report": f"오류 발생: {str(e)}"}), 500

# 테스트 API
@app.route('/api/test')
def test_api():
    return jsonify({"status": "success", "message": "API 서버가 정상 작동 중입니다."})

# 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)