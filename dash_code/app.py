# 파일명: app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, g, logging as flask_logging
import os
import sys #모듈추가 
import json  # JSON 파싱을 위해 추가
import logging
import pandas as pd
from datetime import timedelta, datetime
from core.news_analyzer import NewsAnalyzer

# 기능 모듈 임포트
from app_modules import DashboardModule, NewsModule, MusinsaModule, MagazineModule

# 로깅 설정을 먼저 실행
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 통합된 all3의 config import
import core.config as app_config

# --- RAG 시스템 관련 import 및 초기화 ---
# 여러 경로 시도 (절대 경로 및 상대 경로)
rag_system = None
rag_system_initialized = False
searcher_paths = [
    '/Users/Admin/Desktop/rag/검색기',  # 절대 경로
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '검색기')),  # 상대 경로 (app.py 파일 기준)
    os.path.join(os.getcwd(), '..', '검색기')  # 현재 작업 디렉토리 기준
]

# 각 경로를 시도하며 유효한 경로 찾기
searcher_path = None
for path in searcher_paths:
    if os.path.isdir(path):
        searcher_path = path
        logger.info(f"'검색기' 폴더를 찾았습니다: {path}")
        break

if not searcher_path:
    logger.error(f"CRITICAL: '검색기' 폴더를 찾을 수 없습니다. 시도한 경로: {searcher_paths}")
else:
    # sys.path에 추가하여 모듈 import 가능하게 함
    if searcher_path not in sys.path:
        sys.path.insert(0, searcher_path)  # 우선순위를 높이기 위해 맨 앞에 추가
        logger.info(f"sys.path에 '검색기' 경로 추가: {searcher_path}")

    try:
        from modi_rag import ModiRagSystem
        print("--- RAG 시스템 초기화 시작 ---") # 초기화 시작 로그 추가
        # RAG 시스템 초기화 시 통합된 app_config 사용
        rag_system = ModiRagSystem(llm_api_key=app_config.LLM_API_KEY, llm_api_url=app_config.LLM_API_URL)
        print("ModiRagSystem 객체 생성 완료.")

        # --- 데이터 로딩 코드 추가 ---
        try:
            print("--- RAG 시스템 데이터 로딩 시작 ---")
            # 설정 파일(app_config)에 정의된 경로 사용
            rag_system.load_data(
                fashion_path=app_config.FASHION_DOC_PATH,
                musinsa_path=app_config.MUSINSA_DOC_PATH,
                doc_vecs_path=app_config.DOC_VECS_PATH,
                ent_vecs_path=app_config.ENT_VECS_PATH
            )
            # 날짜 데이터 확인 및 할당 (데이터 로드 후 실행)
            print("날짜 데이터 처리 시작...") # 날짜 처리 로그 추가
            rag_system.ensure_date_data()
            print("--- RAG 시스템 데이터 로딩 및 날짜 할당 완료 ---")
            rag_system_initialized = True # 데이터 로드 성공 시 초기화 완료로 간주
            logger.info("RAG 시스템 초기화 및 데이터 로드 완료 (all3/app.py)")
        except FileNotFoundError as fnf_error:
            logger.error(f"RAG 데이터 파일 로딩 실패 (파일 없음): {fnf_error}", exc_info=True)
            rag_system_initialized = False
        except Exception as load_e:
            logger.error(f"RAG 시스템 데이터 로딩 실패 (기타 오류): {load_e}", exc_info=True)
            rag_system_initialized = False # 데이터 로드 실패 시 초기화 실패로 간주
        # --- 데이터 로딩 코드 끝 ---

    except ImportError as e:
        logger.error(f"RAG 시스템 모듈 import 실패: {e}. '검색기' 폴더 내 modi_rag.py 파일을 확인하세요.", exc_info=True)
        logger.debug(f"현재 sys.path: {sys.path}")
    except Exception as e:
        logger.error(f"RAG 시스템 초기화 실패 (all3/app.py): {e}", exc_info=True)
# --- RAG 시스템 관련 코드 끝 ---


# NewsAnalyzer 인스턴스 생성
news_analyzer = NewsAnalyzer()

# 로깅 설정 - 디버그 레벨로 변경
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 데이터 디렉토리 생성
DATA_DIR = os.path.join('data')
os.makedirs(DATA_DIR, exist_ok=True)

# 정적 파일 디렉토리 생성
STATIC_DIR = os.path.join('static', 'images')
os.makedirs(STATIC_DIR, exist_ok=True)

# 경쟁사 이미지 디렉토리 생성
COMPETITOR_DIR = os.path.join('static', 'images', 'competitor')
os.makedirs(COMPETITOR_DIR, exist_ok=True)

# Flask 애플리케이션 생성
app = Flask(__name__, 
            static_folder='static',  # 프로젝트 루트의 static 폴더 지정
            static_url_path='/static')  # URL 경로 명시적 설정
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

# 정적 파일 요청 로깅 활성화
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['DEBUG'] = True

# 기능 모듈 초기화
dashboard_module = DashboardModule()
news_module = NewsModule()
musinsa_module = MusinsaModule()
magazine_module = MagazineModule()

# --- LLM 응답 파싱 함수 추가 ---
def parse_llm_report(report_content: str) -> dict:
    """LLM이 생성한 레포트를 파싱하여 딕셔너리로 반환"""
    parsed_data = {
        'trendInsight': '파싱된 트렌드 인사이트 예시',
        'buyingInsight': {'summary': '파싱된 바잉 요약', 'recommendations': [{'category': '상의', 'name': '파싱된 아이템', 'reason': '파싱된 이유'}]},
        'sellingInsight': {'summary': '파싱된 셀링 요약', 'keywords': [{'text': '파싱키워드', 'stats': '파싱 통계'}]},
        'keywordReports': []  # 상세 리포트 파싱 로직 추가 필요
    }

    try:
        # 간단한 마크다운 섹션 파싱 예시
        sections = report_content.split('###')
        for section in sections:
            section = section.strip()
            if section.startswith('📌 인기 키워드'):
                pass  # 이미 topKeywords로 처리됨
            elif section.startswith('🧠 리포트 작성 지시사항'):
                break  # 지시사항 이후는 파싱 대상 아님
            elif section.startswith('1. [트렌드 키워드 및 설명]'):
                # 첫 줄 제외하고 내용 추출
                lines = section.split('\n', 1)
                if len(lines) > 1:
                    parsed_data['trendInsight'] = lines[1].strip()
            elif section.startswith('8. [바잉 MD 전략 제안]'):
                lines = section.split('\n', 1)
                if len(lines) > 1:
                    # 바잉/셀링 인사이트는 더 복잡한 파싱 필요
                    # 여기서는 임시로 요약만 넣음
                    parsed_data['buyingInsight']['summary'] = lines[1].strip()[:100] + "..."  # 첫 100자만 사용
                    parsed_data['sellingInsight']['summary'] = lines[1].strip()[:100] + "..."  # 첫 100자만 사용

        # 간단한 예시 키워드 리포트 추가
        for i in range(5):
            parsed_data['keywordReports'].append({
                'keyword': f'키워드{i+1}',
                'summary': f'키워드{i+1}에 대한 상세 분석 내용입니다.'
            })

    except Exception as parse_error:
        logger.error(f"LLM 레포트 파싱 오류: {parse_error}")
        # 파싱 실패 시 기본값 유지

    # 기본값이 없는 경우 채우기
    parsed_data.setdefault('trendInsight', '트렌드 인사이트 분석 중 오류가 발생했습니다.')
    parsed_data.setdefault('buyingInsight', {'summary': '바잉 인사이트 분석 중 오류', 'recommendations': []})
    parsed_data.setdefault('sellingInsight', {'summary': '셀링 인사이트 분석 중 오류', 'keywords': []})
    parsed_data.setdefault('keywordReports', [{'keyword': f'키워드{i+1}', 'summary': '상세 리포트 분석 중 오류'} for i in range(5)])

    return parsed_data
# --- 파싱 함수 끝 ---

# 기능 모듈 초기화
dashboard_module = DashboardModule()
news_module = NewsModule()
musinsa_module = MusinsaModule()
magazine_module = MagazineModule()

@app.before_request
def set_global_period():
    """모든 요청 전에 실행되는 함수, 전역 기간 설정"""
    # 정적 파일 요청은 처리하지 않음
    if request.path.startswith('/static/'):
        return
        
    # URL에서 period 파라미터 가져오기
    g.period = request.args.get('period', '7일')
    g.start_date = request.args.get('start_date')
    g.end_date = request.args.get('end_date')
    
    # 디버그 로깅 - 요청 정보
    logger.debug(f"요청 경로: {request.path}, 요청 인자: {dict(request.args)}")
    
    # 유효한 period 값 확인
    valid_periods = ['7일', '2주', '1개월', '3개월', '6개월', '1년', '1주일', 'custom']
    if g.period not in valid_periods:
        logger.warning(f"지원하지 않는 기간({g.period})이 요청되어 기본값(7일)으로 설정합니다.")
        g.period = '7일'
    
    # custom 기간 설정 시 start_date와 end_date 확인
    if g.period == 'custom' and (not g.start_date or not g.end_date):
        logger.warning("custom 기간이 선택되었으나 시작일 또는 종료일이 없어 기본값(7일)으로 설정합니다.")
        g.period = '7일'
        g.start_date = None
        g.end_date = None
    
    logger.info(f"전역 기간 설정: period={g.period}, start_date={g.start_date}, end_date={g.end_date}")

@app.before_request
def log_request_info():
    # 정적 파일 요청인 경우만 로깅
    if request.path.startswith('/static/'):
        logger.debug(f"정적 파일 요청: {request.path}")

# 정적 파일 디렉토리 인덱싱 요청 처리
@app.route('/static/')
@app.route('/static/<path:directory>')
def handle_directory_index(directory=''):
    """정적 파일 디렉토리 인덱스 요청 처리"""
    if not directory or directory.endswith('/'):
        logger.debug(f"정적 디렉토리 인덱스 요청 리다이렉트: {directory}")
        # 메인 페이지로 리다이렉트
        return redirect(url_for('dashboard'))
    return app.send_static_file(directory)

@app.route('/')
def index():
    """메인 페이지 - 대시보드로 리다이렉트"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """통합 대시보드"""
    try:
        # 기간 설정
        if g.period == 'custom' and g.start_date and g.end_date:
            period = 'custom'
            start_date = g.start_date
            end_date = g.end_date
        else:
            period = g.period
            start_date = None
            end_date = None

                # 현재 시간 (캐시 방지용)
        now = datetime.now()

        # RAG 시스템 초기화 실패 시 에러 메시지 전달
        if not rag_system_initialized:
            error_msg = "데이터 분석 시스템 초기화에 실패했습니다. 관리자에게 문의하세요."
            return render_template('dashboard.html',
                               error=error_msg,
                               period=period,
                               display_period=display_period,
                               start_date=start_date,
                               end_date=end_date,
                               now=now)
        
        # 현재 시간 (캐시 방지용)
        now = datetime.now()
        
        # 데이터 로더 초기화
        news_data_loader = news_module.data_loader
        magazine_data_loader = magazine_module.data_loader
        musinsa_data_loader = musinsa_module.data_loader
        
        # 데이터 로드
        if period == 'custom' and start_date and end_date:
            data = news_data_loader.load_data_by_date_range(start_date, end_date)
            magazine_data = magazine_data_loader.load_data_by_date_range(start_date, end_date)
            musinsa_data = musinsa_data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_data_loader.load_data_by_period(period)
            magazine_data = magazine_data_loader.load_data_by_period(period)
            musinsa_data = musinsa_data_loader.load_data_by_period(period)
        
        # 통합 트렌드 API 호출
        api_url = f"/api/integrated-trends?period={period}"
        if period == 'custom' and start_date and end_date:
            api_url += f"&start_date={start_date}&end_date={end_date}"
        
        try:
            # 내부적으로 API 호출 (app_context 내에서 직접 함수 호출)
            with app.test_request_context(api_url):
                trends_data = integrated_trends().get_json()
        except Exception as e:
            logger.error(f"통합 트렌드 API 호출 실패: {e}", exc_info=True)
            trends_data = {}
        
        # 데이터가 없는 경우 처리
        if data is None or data.empty:
            data = pd.DataFrame()  # 빈 DataFrame으로 초기화
        
        # 기존 시각화 데이터 로드
        fig_network = dashboard_module.generate_network_graph(data) if not data.empty else None
        fig_category = dashboard_module.generate_category_chart(data) if not data.empty else None
        fig_wordcloud = dashboard_module.generate_wordcloud(data) if not data.empty else None
        
        # API에서 반환한 데이터 사용
        top_keywords = trends_data.get('topKeywords', [])
        keyword_reports = trends_data.get('keywordReports', [])
        trend_insight = trends_data.get('trendInsight', '')
        buying_insight = trends_data.get('buyingInsight', {}).get('summary', '')
        selling_insight = trends_data.get('sellingInsight', {}).get('summary', '')
        
        # 디스플레이용 기간 문자열
        if period == 'custom' and start_date and end_date:
            display_period = f"{start_date} ~ {end_date}"
        else:
            display_period = period
        
        # 현재 월 정보
        current_month = now.strftime('%Y년 %m월')
        
        return render_template('dashboard.html',
                              period=period,
                              display_period=display_period,
                              start_date=start_date,
                              end_date=end_date,
                              fig_network=fig_network,
                              fig_category=fig_category,
                              fig_wordcloud=fig_wordcloud,
                              top_keywords=top_keywords,
                              keyword_reports=keyword_reports,
                              trend_insight=trend_insight,
                              buying_insight=buying_insight,
                              selling_insight=selling_insight,
                              current_month=current_month,
                              now=now,
                              events=trends_data.get('events', []))
    except Exception as e:
        logger.error(f"대시보드 렌더링 오류: {e}", exc_info=True)
        return render_template('dashboard.html',
                              error="대시보드 로딩 중 오류가 발생했습니다.",
                              period=g.period,
                              start_date=g.start_date,
                              end_date=g.end_date,
                              now=datetime.now())

@app.route('/news')
def news():
    """뉴스 분석 페이지"""
    try:
        # 입력값 검증
        if g.period == 'custom':
            if not (g.start_date and g.end_date) or g.start_date == 'None' or g.end_date == 'None':
                # 현재 날짜와 30일 전 날짜를 기본값으로 설정
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                # 기본 기간으로 변경
                g.period = '1개월'
                logger.info(f"날짜 None 값 대신 기본값 사용: {start_date} ~ {end_date}")
            else:
                try:
                    start_date = pd.to_datetime(g.start_date).strftime('%Y-%m-%d')
                    end_date = pd.to_datetime(g.end_date).strftime('%Y-%m-%d')
                except Exception as e:
                    # 현재 날짜와 30일 전 날짜를 기본값으로 설정
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                    # 기본 기간으로 변경
                    g.period = '1개월'
                    logger.warning(f"날짜 형식이 올바르지 않아 기본값 사용: {e}")
                
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
            display_period = f"{start_date} ~ {end_date}"
            # ...기존 코드...
        else:
            if g.period not in ['7일', '2주', '1개월', '3개월', '6개월', '1년']:
                logger.warning(f"지원하지 않는 기간: {g.period}, 기본값 '7일'로 설정")
                g.period = '7일'
            data = news_module.data_loader.load_data_by_period(g.period)
            display_period = g.period

        # 현재 시간 추가 (JS 캐시 방지용)
        from datetime import datetime
        now = datetime.now()

        if data is None or data.empty:
            return render_template('news.html',
                               error="해당 기간에 데이터가 없습니다.",
                               period=g.period,
                               start_date=g.start_date,
                               end_date=g.end_date,
                               news_articles=[],
                               now=now)  # 현재 시간 추가

        # NewsAnalyzer에 데이터 설정
        news_module.analyzer.set_data(data)
        
        # 대시보드 데이터 생성
        dashboard_data = news_module.analyzer.generate_dashboard_data()
        
        # 최신 뉴스 기사
        latest_articles = data.sort_values('published', ascending=False).head(10).to_dict('records')
        
        # 상위 키워드 추출
        freq_results = news_module.analyzer.analyze_word_frequency()
        top_keywords = news_module.analyzer.get_top_words(freq_results, top_n=5)
        
        # 감성 분석
        sentiment_df = news_module.analyzer.calculate_article_sentiment()
        sentiment_results = news_module.analyzer.get_sentiment_distribution(sentiment_df)
        
        # 긍정/부정 기사
        positive_articles = sentiment_results['positive_articles'][:3] if sentiment_results else []
        negative_articles = sentiment_results['negative_articles'][:3] if sentiment_results else []
        
        return render_template('news.html',
                            period=g.period,
                            display_period=display_period,
                            start_date=g.start_date,
                            end_date=g.end_date,
                            latest_articles=latest_articles,
                            top_keywords=top_keywords,
                            keyword_trend=dashboard_data.get('keyword_trend'),
                            tfidf_wordcloud=dashboard_data.get('wordcloud'),
                            keyword_network=dashboard_data.get('keyword_network'),
                            positive_articles=positive_articles,
                            negative_articles=negative_articles,
                            now=now)  # 현재 시간 추가

    except ValueError as e:
        logger.error(f"입력값 오류: {e}")
        return render_template('news.html',
                            error=str(e),
                            period=g.period,
                            start_date=g.start_date,
                            end_date=g.end_date,
                            news_articles=[],
                            now=datetime.now())  # 현재 시간 추가
    except Exception as e:
        logger.error(f"뉴스 렌더링 중 오류 발생: {e}", exc_info=True)
        return render_template('news.html',
                            error="데이터 처리 중 오류가 발생했습니다.",
                            period=g.period,
                            start_date=g.start_date,
                            end_date=g.end_date,
                            news_articles=[],
                            now=datetime.now())  # 현재 시간 추가

@app.route('/musinsa')
def musinsa():
    """무신사 경쟁사 분석 페이지"""
    try:
        # CSV 직접 로드로 변경
        if g.period == 'custom' and g.start_date and g.end_date:
            return musinsa_module.render_musinsa(
                period='custom', 
                start_date=g.start_date, 
                end_date=g.end_date
            )
        
        return musinsa_module.render_musinsa(period=g.period)
    
    except Exception as e:
        logger.error(f"무신사 페이지 로드 오류: {e}", exc_info=True)
        return render_template('musinsa.html', error="데이터를 로드할 수 없습니다.")

@app.route('/magazine')
def magazine():
    """매거진 분석 페이지"""
    # URL에서 선택된 매거진 가져오기
    selected_magazines = request.args.getlist('magazine')
    
    # 선택된 매거진이 없으면 기본값 설정
    if not selected_magazines:
        selected_magazines = ['jentestore', 'marieclaire', 'vogue', 'wkorea', 'wwdkorea']
    
    if g.period == 'custom' and g.start_date and g.end_date:
        return magazine_module.render_magazine(
            period='custom', 
            start_date=g.start_date, 
            end_date=g.end_date,
            selected_magazines=selected_magazines
        )
    
    return magazine_module.render_magazine(
        period=g.period,
        selected_magazines=selected_magazines
    )

@app.route('/api/keywords')
def get_keywords():
    """키워드 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        data_loader = dashboard_module.data_loader
        
        if period == 'custom' and start_date and end_date:
            data = data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("키워드 API: 데이터가 없습니다.")
            return jsonify([])
        
        all_tokens = []
        if 'tokens' in data.columns:
            for tokens in data['tokens']:
                if isinstance(tokens, list):
                    all_tokens.extend(tokens)
        
        if not all_tokens:
            logger.warning("키워드 API: 토큰 데이터가 없습니다.")
            return jsonify([])
            
        token_counts = pd.Series(all_tokens).value_counts().head(20)
        
        keywords = [{'text': key, 'count': int(value)} 
                   for key, value in token_counts.items()]
        
        return jsonify(keywords)
    
    except Exception as e:
        logger.error(f"키워드 API 오류: {e}")
        return jsonify([])

@app.route('/api/magazine-data')
def get_magazine_data():
    """매거진 데이터 API"""
    try:
        magazine = request.args.get('magazine')
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        if not magazine:
            return jsonify({'error': '매거진 이름이 필요합니다.'})
        
        data_loader = magazine_module.data_loader
        
        if period == 'custom' and start_date and end_date:
            data = data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = data_loader.load_data_by_period(period)
            
        if data is None or data.empty:
            logger.warning(f"매거진 데이터 API: {magazine}에 대한 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        keywords = data_loader.get_magazine_keywords(magazine)
        card_news = data_loader.get_card_news(magazine)
        
        return jsonify({
            'keywords': keywords,
            'card_news': card_news
        })
    
    except Exception as e:
        logger.error(f"매거진 데이터 API 오류: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/category-data')
def category_data():
    """카테고리별 데이터 API"""
    try:
        # 요청 파라미터 로깅 (디버깅용)
        logger.debug(f"카테고리 데이터 API 요청 파라미터: {dict(request.args)}")
        
        category_type = request.args.get('type', 'item')
        period = request.args.get('period') or g.period
        start_date = request.args.get('start_date') or g.start_date
        end_date = request.args.get('end_date') or g.end_date
        
        logger.info(f"카테고리 데이터 API: 타입={category_type}, 기간={period}, 시작일={start_date}, 종료일={end_date}")
        
        # 데이터 로더 초기화
        data_loader = magazine_module.data_loader
        
        # custom 기간인 경우 시작/종료일 설정
        if period == 'custom' and start_date and end_date:
            data_loader.custom_start_date = start_date
            data_loader.custom_end_date = end_date
            logger.info(f"직접 설정 기간 사용: {start_date} ~ {end_date}")
        
        # 카테고리 데이터 가져오기
        category_data = data_loader.get_category_data(category_type, period)
        
        if not category_data:
            # 샘플 데이터 반환 (데이터가 없는 경우)
            logger.warning(f"카테고리 데이터가 없습니다: 타입={category_type}, 기간={period}")
            return jsonify({
                'categories': ['데이터 없음'],
                'counts': [0],
                'growth_rates': [0],
                'prev_counts': [0]
            })
        
        return jsonify(category_data)
    
    except Exception as e:
        logger.error(f"카테고리 데이터 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})
    
@app.route('/api/brand-details')
def brand_details():
    try:
        brand_name = request.args.get('brand')
        if not brand_name:
            return jsonify({"error": "브랜드명이 필요합니다."}), 400
        
        # 데이터 캐싱 고려
        file_path = os.path.join('data', 'musinsa_data.csv')
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # 데이터 안전하게 처리
        brand_data = df[df['brand'] == brand_name]
        
        if brand_data.empty:
            return jsonify({"error": f"{brand_name} 브랜드 데이터가 없습니다."}), 404
        
        details = {
            'name': brand_name,
            'category': _get_safe_mode(brand_data['category']),
            'gender': _get_safe_unique_list(brand_data['gender']),
            'price_info': _get_price_range_info(brand_data),
            'rating_info': _get_rating_info(brand_data),
            'review_info': _get_review_info(brand_data),
            'product_details': _get_product_sample(brand_data)
        }
        
        return jsonify(details)
    
    except Exception as e:
        logger.error(f"브랜드 상세 정보 조회 오류: {e}")
        return jsonify({"error": "서버 처리 중 오류가 발생했습니다."}), 500

def _get_safe_mode(series):
    """시리즈의 최빈값을 안전하게 반환"""
    try:
        return series.mode().values[0] if not series.empty else "정보 없음"
    except:
        return "정보 없음"

def _get_safe_unique_list(series):
    """고유값 리스트를 안전하게 반환"""
    try:
        unique_values = series.unique().tolist()
        return unique_values if unique_values else ["정보 없음"]
    except:
        return ["정보 없음"]

def _get_price_range_info(brand_data):
    """가격 정보 안전하게 추출"""
    try:
        # 가격 문자열에서 숫자 추출
        prices = brand_data['price'].str.replace(',', '').str.replace('원', '').astype(int)
        return {
            'min_price': f"{prices.min():,}원",
            'max_price': f"{prices.max():,}원",
            'avg_price': f"{int(prices.mean()):,}원"
        }
    except Exception as e:
        logger.warning(f"가격 정보 추출 오류: {e}")
        return {
            'min_price': '정보 없음',
            'max_price': '정보 없음', 
            'avg_price': '정보 없음'
        }

def _get_rating_info(brand_data):
    """평점 정보 안전하게 추출"""
    try:
        return {
            'avg_rating': f"{brand_data['rating'].mean():.2f}",
            'rating_count': len(brand_data[brand_data['rating'] > 0])
        }
    except Exception as e:
        logger.warning(f"평점 정보 추출 오류: {e}")
        return {
            'avg_rating': '0.00',
            'rating_count': 0
        }

def _get_review_info(brand_data):
    """리뷰 정보 안전하게 추출"""
    try:
        return {
            'total_reviews': int(brand_data['review_count'].sum()),
            'avg_reviews_per_product': f"{brand_data['review_count'].mean():.1f}"
        }
    except Exception as e:
        logger.warning(f"리뷰 정보 추출 오류: {e}")
        return {
            'total_reviews': 0,
            'avg_reviews_per_product': '0.0'
        }

def _get_product_sample(brand_data, n=5):
    """대표 상품 샘플 안전하게 추출"""
    try:
        # 리뷰 많은 순으로 정렬 후 샘플 추출
        sample_products = []
        sorted_data = brand_data.sort_values('review_count', ascending=False).head(n)
        
        for _, row in sorted_data.iterrows():
            sample_products.append({
                'name': row.get('name', '상품명 없음'),
                'price': row.get('price', '가격 정보 없음'),
                'review_count': int(row.get('review_count', 0)),
                'link': row.get('link', '#')
            })
        
        return sample_products
    except Exception as e:
        logger.warning(f"대표 상품 추출 오류: {e}")
        return []

#뉴스 관련 라우트 추가
@app.route('/api/news/tfidf')
def api_news_tfidf():
    """뉴스 TF-IDF 분석 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("TF-IDF API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # NewsAnalyzer에 데이터 설정
        news_analyzer.set_data(data)
        
        # TF-IDF 분석 실행
        tfidf_results = news_analyzer.analyze_tfidf()
        
        # TF-IDF 차트 생성
        tfidf_chart = news_analyzer.generate_tfidf_chart(top_n=20, tfidf_results=tfidf_results)
        
        # TF-IDF 워드클라우드 생성
        tfidf_wordcloud = news_analyzer.generate_tfidf_wordcloud(tfidf_results=tfidf_results)
        
        # 결과 반환
        result = {
            'chart': tfidf_chart,
            'wordcloud': tfidf_wordcloud
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"TF-IDF API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/news/topics')
def api_news_topics():
    """뉴스 토픽 모델링 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("토픽 모델링 API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # NewsAnalyzer에 데이터 설정
        news_analyzer.set_data(data)
        
        # 토픽 개수 파라미터
        n_topics = request.args.get('n_topics', default=5, type=int)
        
        # 토픽 모델링 실행
        topic_results = news_analyzer.analyze_topics(n_topics=n_topics)
        
        # 토픽 분포 정보
        topic_distribution = news_analyzer.get_topic_distribution(topic_results)
        
        # 토픽 차트 생성
        topic_charts = news_analyzer.generate_topic_chart(topic_results)
        
        # 결과 반환
        result = {
            'topic_info': topic_distribution['topic_info'] if topic_distribution else None,
            'charts': topic_charts
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"토픽 모델링 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/news/sentiment')
def api_news_sentiment():
    """뉴스 감성 분석 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("감성 분석 API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # NewsAnalyzer에 데이터 설정
        news_analyzer.set_data(data)
        
        # 감성 분석 실행
        sentiment_df = news_analyzer.calculate_article_sentiment()
        
        # 감성 분포 정보
        sentiment_distribution = news_analyzer.get_sentiment_distribution(sentiment_df)
        
        # 감성 차트 생성
        sentiment_charts = news_analyzer.generate_sentiment_chart(sentiment_df)
        
        # 감성 워드클라우드 생성
        sentiment_wordclouds = news_analyzer.get_sentiment_wordcloud(sentiment_df)
        
        # 결과 반환
        result = {
            'sentiment_counts': sentiment_distribution['sentiment_counts'] if sentiment_distribution else None,
            'positive_articles': sentiment_distribution['positive_articles'][:3] if sentiment_distribution else [],
            'negative_articles': sentiment_distribution['negative_articles'][:3] if sentiment_distribution else [],
            'charts': sentiment_charts,
            'wordclouds': sentiment_wordclouds
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"감성 분석 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/news/search')
def api_news_search():
    """뉴스 키워드 검색 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        # 검색 키워드
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({'error': '검색 키워드가 필요합니다.'})
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("검색 API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # 키워드로 기사 필터링
        if 'token_list' in data.columns:
            # 토큰에서 키워드 검색
            matches = data['token_list'].apply(lambda tokens: keyword in tokens if isinstance(tokens, list) else False)
        elif 'tokens' in data.columns:
            # 토큰에서 키워드 검색
            matches = data['tokens'].apply(lambda tokens: keyword in tokens if isinstance(tokens, list) else False)
        else:
            # 제목이나 내용에서 키워드 검색
            matches = (
                data['title'].str.contains(keyword, case=False, na=False) | 
                data['content'].str.contains(keyword, case=False, na=False)
            )
        
        matched_articles = data[matches].sort_values('upload_date', ascending=False)
        
        # 결과 반환
        result = {
            'keyword': keyword,
            'total_matches': len(matched_articles),
            'articles': matched_articles.head(10).to_dict('records')
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"검색 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/news/network')
def api_news_network():
    """뉴스 단어 연관성 네트워크 API"""
    try:
        period = g.period
        start_date = g.start_date
        end_date = g.end_date
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("네트워크 API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # NewsAnalyzer에 데이터 설정
        news_analyzer.set_data(data)
        
        # 연관성 분석 실행
        association_results = news_analyzer.analyze_word_association()
        
        # 중심 단어 추출
        central_words = news_analyzer.get_central_words(association_results)
        
        # 네트워크 그래프 생성
        network_graph = news_analyzer.generate_network_graph(association_results)
        
        # 결과 반환
        result = {
            'central_words': central_words,
            'network_graph': network_graph
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"네트워크 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/news/trend')
def api_news_trend():
    """뉴스 시계열 트렌드 API"""
    try:
        # 요청 파라미터 직접 가져오기
        period = request.args.get('period', g.period)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # None 값 확인 및 처리
        if start_date == 'None' or start_date == '' or start_date is None:
            # 기본값으로 변경
            if period == 'custom':
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                period = '1개월'  # 기본 기간으로 변경
                logger.info(f"API: 날짜 None 값 대신 기본값 사용: {start_date} ~ {end_date}")
            else:
                start_date = None
        
        if end_date == 'None' or end_date == '' or end_date is None:
            if period == 'custom':
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                period = '1개월'  # 기본 기간으로 변경
                logger.info(f"API: 날짜 None 값 대신 기본값 사용: {start_date} ~ {end_date}")
            else:
                end_date = None
        
        logger.info(f"시계열 트렌드 API 호출: 기간={period}, 시작일={start_date}, 종료일={end_date}")
        
        # NewsModule에서 데이터 로드
        data = None
        
        if period == 'custom' and start_date and end_date:
            try:
                # 날짜 형식 검증
                pd.to_datetime(start_date)
                pd.to_datetime(end_date)
                data = news_module.data_loader.load_data_by_date_range(start_date, end_date)
            except Exception as e:
                logger.error(f"날짜 형식 오류: {e}")
                return jsonify({'error': f'날짜 형식이 올바르지 않습니다: {e}'})
        else:
            data = news_module.data_loader.load_data_by_period(period)
        
        if data is None or data.empty:
            logger.warning("트렌드 API: 데이터가 없습니다.")
            return jsonify({'error': '데이터가 없습니다.'})
        
        # NewsAnalyzer에 데이터 설정
        news_analyzer.set_data(data)
        
        # 시계열 단위
        time_unit = request.args.get('unit', default='monthly')
        
        logger.info(f"시계열 분석 단위: {time_unit}")
        
        # 시계열 분석 실행
        time_data = news_analyzer.analyze_time_series()
        
        if not time_data:
            logger.warning("시계열 데이터 생성 실패")
            return jsonify({'error': '시계열 데이터를 생성할 수 없습니다.'})
        
        # 시계열 차트 생성
        time_chart = news_analyzer.generate_time_series_chart(time_data=time_data, time_unit=time_unit)
        
        # 키워드 트렌드 (상위 5개 키워드)
        top_keywords = []
        
        try:
            freq_results = news_analyzer.analyze_word_frequency()
            
            if not freq_results or 'word_counts' not in freq_results:
                logger.warning("단어 빈도 분석 결과가 없습니다.")
                return jsonify({
                    'time_chart': time_chart,
                    'error': '키워드 분석 결과가 없습니다.'
                })
            
            top_keywords = [word for word, _ in freq_results['word_counts'].most_common(5)]
            
            logger.info(f"상위 키워드: {top_keywords}")
            
            # 키워드 트렌드 분석 (개선된 버전)
            keyword_trend_data = news_analyzer.analyze_keyword_trend(top_keywords, time_unit)
            
            if keyword_trend_data is None:
                logger.warning("키워드 트렌드 데이터가 None입니다.")
                return jsonify({
                    'time_chart': time_chart,
                    'error': '키워드 트렌드 데이터를 생성할 수 없습니다.',
                    'top_keywords': top_keywords
                })
            
            # 데이터 구조 로깅
            if keyword_trend_data:
                logger.info(f"키워드 트렌드 데이터 구조: {list(keyword_trend_data.keys())}")
                if 'trends' in keyword_trend_data:
                    logger.info(f"트렌드 키: {list(keyword_trend_data['trends'].keys())}")
            
            # 키워드 트렌드 차트 생성 (개선된 버전)
            keyword_trend_chart = news_analyzer.generate_keyword_trend_chart(top_keywords, keyword_trend_data)
            
            if keyword_trend_chart is None:
                logger.warning("키워드 트렌드 차트 생성 실패")
                return jsonify({
                    'time_chart': time_chart,
                    'error': '키워드 트렌드 차트를 생성할 수 없습니다.',
                    'top_keywords': top_keywords
                })
            
            logger.info(f"키워드 트렌드 차트 생성 완료")
            
        except Exception as e:
            logger.error(f"키워드 트렌드 분석 중 오류: {e}", exc_info=True)
            return jsonify({
                'time_chart': time_chart,
                'error': f'키워드 트렌드 분석 중 오류: {str(e)}',
                'top_keywords': top_keywords
            })
        
        # 결과 반환
        result = {
            'time_chart': time_chart,
            'keyword_trend': keyword_trend_chart,
            'top_keywords': top_keywords
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"트렌드 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})
    
# app.py에 추가할 라우트

@app.route('/api/integrated-trends')
def integrated_trends():
    """통합 트렌드 분석 API"""
    try:
        # 요청 파라미터
        period = request.args.get('period', '7일')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        logger.info(f"통합 트렌드 요청: 기간={period}, 시작일={start_date}, 종료일={end_date}")
        
        # 데이터 로더 초기화
        news_data_loader = news_module.data_loader
        magazine_data_loader = magazine_module.data_loader
        musinsa_data_loader = musinsa_module.data_loader
        
        # 데이터 로드
        if period == 'custom' and start_date and end_date:
            news_data = news_data_loader.load_data_by_date_range(start_date, end_date)
            magazine_data = magazine_data_loader.load_data_by_date_range(start_date, end_date)
            musinsa_data = musinsa_module.data_loader.load_data_by_date_range(start_date, end_date)
        else:
            news_data = news_data_loader.load_data_by_period(period)
            magazine_data = magazine_data_loader.load_data_by_period(period)
            musinsa_data = musinsa_module.data_loader.load_data_by_period(period)
        
        # 데이터 유효성 검사
        if news_data is None or news_data.empty:
            logger.warning("뉴스 데이터가 없습니다.")
            news_data = pd.DataFrame()
        
        if magazine_data is None or magazine_data.empty:
            logger.warning("매거진 데이터가 없습니다.")
            magazine_data = pd.DataFrame()
            
        if musinsa_data is None or musinsa_data.empty:
            logger.warning("무신사 데이터가 없습니다.")
            musinsa_data = pd.DataFrame()
        
        # 모든 데이터가 비어있는 경우
        if news_data.empty and magazine_data.empty and musinsa_data.empty:
            return jsonify({
                'error': '해당 기간에 데이터가 없습니다.',
                'topKeywords': []
            })
        
        # 통합 데이터 준비
        combined_tokens = []
        
        # 뉴스 토큰 추출
        if not news_data.empty and 'token_list' in news_data.columns:
            for tokens in news_data['token_list']:
                if isinstance(tokens, list):
                    combined_tokens.extend(tokens)
        
        # 매거진 토큰 추출
        if not magazine_data.empty and 'tokens' in magazine_data.columns:
            for tokens in magazine_data['tokens']:
                if isinstance(tokens, list):
                    combined_tokens.extend(tokens)
        
        # 무신사 토큰 추출 (적절한 컬럼명 가정)
        if not musinsa_data.empty and 'tokens' in musinsa_data.columns:
            for tokens in musinsa_data['tokens']:
                if isinstance(tokens, list):
                    combined_tokens.extend(tokens)
        
        # 상위 키워드 추출
        from collections import Counter
        token_counter = Counter(combined_tokens)
        top_keywords = token_counter.most_common(10)
        
        # GPT/Gemini API를 호출하여 키워드 분석 및 인사이트 생성 (실제 구현 필요)
        # 여기서는 예시 데이터 반환
        
        # 예시 응답 데이터
        response_data = {
            'topKeywords': [
                {'text': kw, 'count': count, 'description': f"'{kw}' 키워드는 현재 트렌드에서 주목받고 있습니다."} 
                for kw, count in top_keywords
            ],
            'trendInsight': "현재 트렌드 키워드를 분석한 결과, 이번 시즌에는 미니멀한 디자인과 지속가능한 패션이 주목받고 있습니다.",
            'buyingInsight': {
                'summary': "트렌드 분석 결과, 다음 상품들이 주목받을 것으로 예측됩니다:",
                'recommendations': [
                    {'category': '아우터', 'name': '오버사이즈 재킷', 'reason': 'S/S 시즌 트렌드 부상 중'},
                    {'category': '상의', 'name': '니트 베스트', 'reason': '언급량 전월 대비 82% 증가'},
                    {'category': '하의', 'name': '와이드 팬츠', 'reason': '지속적인 인기 유지'}
                ]
            },
            'sellingInsight': {
                'summary': "현재 트렌드와 검색량을 분석한 결과, 다음 키워드를 활용한 마케팅이 효과적일 것으로 예측됩니다:",
                'keywords': [
                    {'text': '미니멀룩', 'stats': '검색량 증가율: +45%'},
                    {'text': '오버핏', 'stats': '검색량 증가율: +38%'},
                    {'text': '뉴트로', 'stats': '검색량 증가율: +27%'}
                ]
            },
            'keywordReports': [
                {
                    'keyword': top_keywords[0][0] if top_keywords else '키워드1',
                    'summary': f"이 키워드는 최근 {period} 동안 주목받고 있으며, 특히 20-30대 여성 소비자들 사이에서 인기가 높습니다. 관련 제품의 수요는 전월 대비 25% 증가했으며, 소셜 미디어에서의 언급량도 지속적으로 증가하고 있습니다."
                },
                {
                    'keyword': top_keywords[1][0] if len(top_keywords) > 1 else '키워드2',
                    'summary': f"이 키워드는 최근 {period} 동안 트렌드로 부상하였으며, 인스타그램에서 관련 해시태그 사용량이 증가하고 있습니다. 주로 10-20대 MZ세대가 관심을 보이고 있으며, 관련 콘텐츠의 참여율도 높습니다."
                },
                {
                    'keyword': top_keywords[2][0] if len(top_keywords) > 2 else '키워드3',
                    'summary': f"이 키워드는 최근 {period} 동안 지속적인 관심을 받고 있으며, 특히 유튜브와 같은 영상 콘텐츠에서 자주 언급되고 있습니다. 남성 소비자층에서도 인기가 증가하는 추세입니다."
                },
                {
                    'keyword': top_keywords[3][0] if len(top_keywords) > 3 else '키워드4',
                    'summary': "해당 키워드는 계절적 요인과 연관이 있으며, 최근 패션 인플루언서들의 소개로 인해 노출이 증가하고 있습니다. 특히 30-40대 소비자층에서 반응이 좋습니다."
                },
                {
                    'keyword': top_keywords[4][0] if len(top_keywords) > 4 else '키워드5',
                    'summary': "이 키워드는 최근 셀럽들의 착용으로 인해 주목받고 있으며, 럭셔리 브랜드와 SPA 브랜드 모두에서 관련 제품이 출시되고 있습니다. 가격대별 다양한 옵션이 소비자들에게 인기를 끌고 있습니다."
                }
            ]
        }
        
        # 캘린더 이벤트 예시 (실제 구현에서는 DB에서 가져오기)
        events = [
            {
                'date': '2025-04-03',
                'title': '서울패션위크 2025 F/W',
                'location': '동대문 DDP',
                'duration': '2025-04-03 ~ 2025-04-08'
            },
            {
                'date': '2025-04-15',
                'title': '패션 아트 전시회',
                'location': '성수동 S팩토리',
                'duration': '2025-04-15 ~ 2025-04-20'
            },
            {
                'date': '2025-04-25',
                'title': '지속가능 패션 포럼',
                'location': '코엑스 컨퍼런스룸',
                'duration': '2025-04-25'
            }
        ]
        
        response_data['events'] = events
        
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"통합 트렌드 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})

@app.route('/api/calendar-events')
def calendar_events():
    """패션 관련 일정 API"""
    try:
        # 요청 파라미터
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        logger.info(f"캘린더 이벤트 요청: 년={year}, 월={month}")
        
        # 여기서는 예시 데이터 반환 (실제 구현에서는 DB에서 가져오기)
        events = []
        
        # 4월 예시 데이터
        if month == 4 and year == 2025:
            events = [
                {
                    'date': datetime(2025, 4, 3).strftime('%Y-%m-%d'),
                    'title': '서울패션위크 2025 F/W',
                    'location': '동대문 DDP',
                    'duration': '2025-04-03 ~ 2025-04-08'
                },
                {
                    'date': datetime(2025, 4, 15).strftime('%Y-%m-%d'),
                    'title': '패션 아트 전시회',
                    'location': '성수동 S팩토리',
                    'duration': '2025-04-15 ~ 2025-04-20'
                },
                {
                    'date': datetime(2025, 4, 25).strftime('%Y-%m-%d'),
                    'title': '지속가능 패션 포럼',
                    'location': '코엑스 컨퍼런스룸',
                    'duration': '2025-04-25'
                }
            ]
        # 5월 예시 데이터
        elif month == 5 and year == 2025:
            events = [
                {
                    'date': datetime(2025, 5, 10).strftime('%Y-%m-%d'),
                    'title': '메트 갈라 2025',
                    'location': '뉴욕 메트로폴리탄 뮤지엄',
                    'duration': '2025-05-10'
                },
                {
                    'date': datetime(2025, 5, 20).strftime('%Y-%m-%d'),
                    'title': '패션 서스테이너빌리티 전시회',
                    'location': '서울 예술의전당',
                    'duration': '2025-05-20 ~ 2025-05-25'
                }
            ]
        
        return jsonify({
            'year': year,
            'month': month,
            'events': events
        })
    
    except Exception as e:
        logger.error(f"캘린더 이벤트 API 오류: {e}", exc_info=True)
        return jsonify({'error': str(e)})


@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query', '')
    data_source = data.get('data_source', 'magazine')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    try:
        # RAG 질의응답 시스템 호출
        response = rag_system.answer_query(
            query=query,
            data_source=data_source,
            start_date=start_date,
            end_date=end_date
        )
        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"질의응답 처리 중 오류: {e}")
        return jsonify({'error': f"질의 처리 중 오류가 발생했습니다: {str(e)}"}), 500


@app.errorhandler(404)
def page_not_found(e):
    """404 오류 처리"""
    error_message = "페이지를 찾을 수 없습니다."
    
    # 정적 파일 요청 오류인 경우 더 구체적인 메시지 제공
    if request.path.startswith('/static/'):
        logger.warning(f"정적 파일을 찾을 수 없음: {request.path}")
        error_message = "요청한 리소스를 찾을 수 없습니다."
        
        # 특정 경로에 대한 문제인 경우 대안 제공
        if 'images/competitor/' in request.path:
            error_message += " 해당 기간에 생성된 차트가 없을 수 있습니다. 다른 기간을 선택해 보세요."
    
    return render_template('error.html', 
                          error=error_message,
                          error_code=404), 404

@app.errorhandler(500)
def server_error(e):
    """500 오류 처리"""
    logger.error(f"서버 오류 발생: {e}", exc_info=True)

    error_message = "서버 내부 오류가 발생했습니다."

    # 이미지 생성 또는 정적 파일 관련 오류인 경우
    if hasattr(e, 'description') and 'image' in str(e).lower():
        error_message = "차트 생성 중 오류가 발생했습니다. 데이터를 확인하거나 다른 기간을 선택해 보세요."

    return render_template('error.html',
                           error=error_message,
                           error_code=500), 500

if __name__ == '__main__':
    # 데이터 로드 실패 시 경고 출력
    if not rag_system_initialized:
        print("\n" + "*"*50)
        print("경고: RAG 시스템 데이터 로딩에 실패했습니다.")
        print("챗봇(/api/ask) 및 관련 기능이 정상 작동하지 않을 수 있습니다.")
        print("core/config.py의 RAG 관련 경로 설정 및 데이터 파일 존재 여부를 확인하세요.")
        print("*"*50 + "\n")
    app.run(debug=True, port=5001)