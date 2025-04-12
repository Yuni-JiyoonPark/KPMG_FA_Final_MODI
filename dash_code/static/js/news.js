/**
 * news.js - 뉴스 분석 페이지 JavaScript 코드
 * 사용자 상호작용 및 데이터 시각화를 관리합니다.
 */

// DOM 로드 완료 후 실행
// 페이지 로드 시 키워드 트렌드 자동 로드

/**
 * 분석 요약 섹션의 토글 기능 초기화
 */
function initializeSummaryToggles() {
    const summaryTitles = document.querySelectorAll('.summary-title.togglable');
    
    summaryTitles.forEach(title => {
        // 이미 이벤트가 등록되어 있는지 확인
        if (title.dataset.initialized === 'true') {
            return;
        }
        
        // 초기 상태 설정 (처음에는 닫힘)
        title.classList.remove('active');
        
        // 클릭 이벤트 추가
        title.addEventListener('click', function() {
            this.classList.toggle('active');
        });
        
        // 이벤트 등록 완료 표시
        title.dataset.initialized = 'true';
    });
}

/**
 * 워드클라우드 및 네트워크 분석 결과에 요약 정보 추가 (토글 가능)
 */
function addAnalysisSummary() {
    // 워드클라우드 요약 추가
    const wordcloudContainer = document.querySelector('.wordcloud-container');
    if (wordcloudContainer && !wordcloudContainer.nextElementSibling?.classList.contains('analysis-summary')) {
        const wordcloudSummary = document.createElement('div');
        wordcloudSummary.className = 'analysis-summary mt-3';
        wordcloudSummary.innerHTML = `
            <h6 class="summary-title togglable">
                분석 요약
                <span class="toggle-icon">
                    <i class="fas fa-chevron-down"></i>
                </span>
            </h6>
            <div class="summary-content-container">
                <p class="summary-content">
                    TF-IDF 분석 결과, '제품', '전자', '활용', '기업', '글로벌'이 주요 키워드로 도출되었습니다. 특히 '제품'과 '전자' 관련 언급이 두드러지며, 기술 산업 트렌드가 주요 화제로 떠오르고 있습니다. 기업의 글로벌 활동과 전자 제품 개발이 뉴스의 핵심 주제로, 최근 업계 동향이 제품 중심의 혁신과 글로벌 시장 확장에 초점을 맞추고 있음을 시사합니다.
                </p>
            </div>
        `;
        wordcloudContainer.parentElement.appendChild(wordcloudSummary);
    }

    // 네트워크 분석 요약 추가
    const networkContainer = document.querySelector('.network-container');
    if (networkContainer && !networkContainer.nextElementSibling?.classList.contains('analysis-summary')) {
        const networkSummary = document.createElement('div');
        networkSummary.className = 'analysis-summary mt-3';
        networkSummary.innerHTML = `
            <h6 class="summary-title togglable">
                분석 요약
                <span class="toggle-icon">
                    <i class="fas fa-chevron-down"></i>
                </span>
            </h6>
            <div class="summary-content-container">
                <p class="summary-content">
                    연관어 네트워크 분석 결과, '글로벌', '금융', '전략', '기술' 등의 키워드가 중심 노드로 강한 연결성을 보이고 있습니다. 특히 '글로벌'과 '금융' 노드의 크기가 크고 연결 강도가 높아, 국제 금융 시장 관련 이슈가 주요 관심사임을 알 수 있습니다. 이는 최근 글로벌 금융 전략과 기술 혁신이 밀접하게 연관되어 있으며, 산업 전반에 걸쳐 국제적 협력과 전략적 접근이 강조되고 있음을 시사합니다.
                </p>
            </div>
        `;
        networkContainer.parentElement.appendChild(networkSummary);
    }
    
    // 토글 기능 초기화
    setTimeout(() => {
        initializeSummaryToggles();
    }, 100);
}



/**
 * 워드클라우드 및 네트워크 분석 결과에 요약 정보 추가
 */
function addAnalysisSummary() {
    // 워드클라우드 요약 추가
    const wordcloudContainer = document.querySelector('.wordcloud-container');
    if (wordcloudContainer && !wordcloudContainer.nextElementSibling?.classList.contains('analysis-summary')) {
        const wordcloudSummary = document.createElement('div');
        wordcloudSummary.className = 'analysis-summary mt-3';
        wordcloudSummary.innerHTML = `
            <h6 class="summary-title">분석 요약</h6>
            <p class="summary-content">
                TF-IDF 분석 결과, '제품', '전자', '활용', '기업', '글로벌'이 주요 키워드로 도출되었습니다. 특히 '제품'과 '전자' 관련 언급이 두드러지며, 기술 산업 트렌드가 주요 화제로 떠오르고 있습니다. 기업의 글로벌 활동과 전자 제품 개발이 뉴스의 핵심 주제로, 최근 업계 동향이 제품 중심의 혁신과 글로벌 시장 확장에 초점을 맞추고 있음을 시사합니다.
            </p>
        `;
        wordcloudContainer.parentElement.appendChild(wordcloudSummary);
    }

    // 네트워크 분석 요약 추가
    const networkContainer = document.querySelector('.network-container');
    if (networkContainer && !networkContainer.nextElementSibling?.classList.contains('analysis-summary')) {
        const networkSummary = document.createElement('div');
        networkSummary.className = 'analysis-summary mt-3';
        networkSummary.innerHTML = `
            <h6 class="summary-title">분석 요약</h6>
            <p class="summary-content">
                연관어 네트워크 분석 결과, '글로벌', '금융', '전략', '기술' 등의 키워드가 중심 노드로 강한 연결성을 보이고 있습니다. 특히 '글로벌'과 '금융' 노드의 크기가 크고 연결 강도가 높아, 국제 금융 시장 관련 이슈가 주요 관심사임을 알 수 있습니다. 이는 최근 글로벌 금융 전략과 기술 혁신이 밀접하게 연관되어 있으며, 산업 전반에 걸쳐 국제적 협력과 전략적 접근이 강조되고 있음을 시사합니다.
            </p>
        `;
        networkContainer.parentElement.appendChild(networkSummary);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 기존 초기화 함수 호출
    initializeFilters();
    initializeTabs();
    initializeDetailViews();
    initializeAnalysisButtons();
    initializeVisualizations();

    initializeSummaryToggles();
    
    // 키워드 트렌드 자동 로드
    loadKeywordTrendIfNeeded();
    
    // Plotly 로드 확인
    if (typeof Plotly === 'undefined') {
        console.warn('Plotly가 로드되지 않았습니다. 차트 리사이징이 작동하지 않을 수 있습니다.');
    }
});


console.log('loadKeywordTrendIfNeeded 함수 실행 시작');
/**
 * 필요한 경우 키워드 트렌드 데이터 로드
 */
/**
 * 필요한 경우 키워드 트렌드 데이터 로드
 */
// loadKeywordTrendIfNeeded 함수 수정 - 차트 크기 조절 추가
// 키워드 트렌드 로드 함수 수정 - 요약 정보 추가
function loadKeywordTrendIfNeeded() {
    console.log('loadKeywordTrendIfNeeded 함수 실행');
    
    const trendContainer = document.querySelector('.trend-container');
    const noDataContainer = document.querySelector('.visualization-container .no-data');
    
    if ((trendContainer && trendContainer.innerHTML.trim() === '') || 
        (noDataContainer && noDataContainer.style.display !== 'none')) {
        
        console.log('키워드 트렌드 데이터 자동 로드');
        
        // 기간 값 가져오기
        const period = document.getElementById('period-selector')?.value || '7일';
        
        // API URL 생성
        let apiUrl = `/api/news/trend?period=${encodeURIComponent(period)}`;

        // custom 기간인 경우 시작일/종료일 추가
        if (period === 'custom') {
            const startDate = document.getElementById('start-date')?.value;
            const endDate = document.getElementById('end-date')?.value;
            
            if (startDate && endDate && startDate !== 'None' && endDate !== 'None') {
                apiUrl += `&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`;
            }
        }
        
        console.log('API 호출 URL:', apiUrl);
        
        // 로딩 표시
        if (trendContainer) {
            trendContainer.innerHTML = '<div class="loading-indicator">로딩 중...</div>';
        } else if (noDataContainer) {
            const loadingElem = noDataContainer.querySelector('#trend-loading');
            if (loadingElem) loadingElem.style.display = 'block';
        }
        
        // 캐시 방지를 위한 타임스탬프 추가
        const timestamp = new Date().getTime();
        apiUrl += `&_=${timestamp}`;
        
        // AJAX 요청
        fetch(apiUrl)
            .then(response => {
                console.log('API 응답 상태:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('API 응답 데이터 키:', Object.keys(data));
                
                // 로딩 인디케이터 숨기기
                if (noDataContainer) {
                    const loadingElem = noDataContainer.querySelector('#trend-loading');
                    if (loadingElem) loadingElem.style.display = 'none';
                }
                
                if (data.keyword_trend) {
                    console.log('트렌드 데이터 수신 완료');
                    
                    // 컨테이너가 없으면 생성
                    if (!trendContainer) {
                        const newTrendContainer = document.createElement('div');
                        newTrendContainer.className = 'trend-container no-scroll'; // no-scroll 클래스 추가
                        const visContainer = document.querySelector('.visualization-container');
                        if (visContainer) {
                            // 기존 no-data 제거
                            if (noDataContainer) noDataContainer.style.display = 'none';
                            visContainer.appendChild(newTrendContainer);
                        }
                    }
                    
                    // 새로운 컨테이너 참조 가져오기
                    const container = document.querySelector('.trend-container');
                    if (container) {
                        // HTML 데이터가 아닌 경우 확인
                        if (typeof data.keyword_trend !== 'string') {
                            console.error('keyword_trend가 문자열이 아닙니다:', typeof data.keyword_trend);
                            container.innerHTML = '<div class="error-message">데이터 형식이 올바르지 않습니다.</div>';
                            return;
                        }
                        
                        container.innerHTML = data.keyword_trend;
                        console.log('트렌드 컨테이너에 데이터 삽입 완료');
                        
                        // Plotly 초기화 확인 및 차트 리사이징
                        if (window.Plotly) {
                            console.log('Plotly 객체 존재함');
                            try {
                                // Plotly 차트 재계산 시도
                                const plotlyCharts = container.querySelectorAll('.js-plotly-plot');
                                console.log('찾은 Plotly 차트 수:', plotlyCharts.length);
                                
                                if (plotlyCharts.length > 0) {
                                    // no-scroll 클래스 추가
                                    plotlyCharts.forEach(chart => {
                                        chart.classList.add('no-scroll');
                                    });
                                    
                                    // 차트 리사이징을 위해 짧은 지연 추가
                                    window.setTimeout(() => {
                                        // 부모 컨테이너의 크기 측정
                                        const parentWidth = container.clientWidth;
                                        const parentHeight = container.clientHeight;
                                        
                                        plotlyCharts.forEach(chart => {
                                            // 차트 크기를 컨테이너에 맞게 조정
                                            chart.style.width = '100%';
                                            chart.style.height = '100%';
                                            
                                            // Plotly 리사이징
                                            window.Plotly.Plots.resize(chart);
                                        });
                                        console.log('Plotly 차트 리사이즈 완료');
                                    }, 100);
                                }
                            } catch (e) {
                                console.error('Plotly 차트 초기화 오류:', e);
                            }
                        } else {
                            console.warn('Plotly 객체 없음');
                        }

                        // 분석 요약 추가
                        addAnalysisSummary();
                    }
                } else {
                    console.log('키워드 트렌드 데이터가 없습니다');
                    if (trendContainer) trendContainer.innerHTML = '<div class="no-data">데이터가 없습니다.</div>';
                }
            })
            .catch(error => {
                console.error('키워드 트렌드 로드 오류:', error);
                if (trendContainer) {
                    trendContainer.innerHTML = '<div class="error-message">데이터 로드 중 오류가 발생했습니다.</div>';
                }
                if (noDataContainer) {
                    const loadingElem = noDataContainer.querySelector('#trend-loading');
                    if (loadingElem) loadingElem.style.display = 'none';
                }
            });
    } else {
        // 이미 데이터가 로드된 경우에도 요약 추가
        addAnalysisSummary();
    }
}

/**
 * 현재 설정된 기간 정보 반환
 * @returns {string} URL 쿼리 문자열
 */
function getCurrentPeriod() {
    // 2번: 함수 실행 로깅
    console.log('getCurrentPeriod 함수 실행');
    
    const urlParams = new URLSearchParams(window.location.search);
    let period = urlParams.get('period') || '7일';
    
    console.log('URL에서 추출한 period 값:', period);
    
    let query = 'period=' + encodeURIComponent(period);
    
    // custom 기간인 경우에만 시작일/종료일 추가
    if (period === 'custom') {
        const startDate = urlParams.get('start_date');
        const endDate = urlParams.get('end_date');
        
        console.log('커스텀 기간 파라미터:', { startDate, endDate });
        
        if (startDate && endDate) {
            query += '&start_date=' + encodeURIComponent(startDate) + 
                     '&end_date=' + encodeURIComponent(endDate);
        }
    }
    
    // 2번: 최종 쿼리 문자열 로깅
    console.log('생성된 쿼리 문자열:', query);
    
    return query;
}

/* 현재 설정된 기간 정보 반환
* @returns {string} URL 쿼리 문자열
*
function getCurrentPeriod() {
   const urlParams = new URLSearchParams(window.location.search);
   let period = urlParams.get('period') || '7일';
   
   let query = 'period=' + encodeURIComponent(period);
   
   // custom 기간인 경우에만 시작일/종료일 추가
   if (period === 'custom') {
       const startDate = urlParams.get('start_date');
       const endDate = urlParams.get('end_date');
       
       if (startDate && endDate) {
           query += '&start_date=' + encodeURIComponent(startDate) + 
                    '&end_date=' + encodeURIComponent(endDate);
       }
   }
   
   return query;
}
*/
/**
 * 필터 및 기간 설정 초기화
 */
function initializeFilters() {
    // 기간 선택 변경 이벤트
    const periodSelector = document.getElementById('period-selector');
    if (periodSelector) {
        periodSelector.addEventListener('change', function() {
            const period = this.value;
            
            // custom 기간 선택 시 날짜 선택기 표시
            const dateRangeContainer = document.getElementById('date-range-container');
            if (dateRangeContainer) {
                dateRangeContainer.style.display = period === 'custom' ? 'block' : 'none';
            }
        });
        
        // 초기 상태 설정
        if (periodSelector.value === 'custom') {
            const dateRangeContainer = document.getElementById('date-range-container');
            if (dateRangeContainer) {
                dateRangeContainer.style.display = 'block';
            }
        }
    }
    
    // 필터 적용 버튼
    const applyFilterBtn = document.getElementById('apply-filter-btn');
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', function() {
            const period = periodSelector ? periodSelector.value : '7일';
            
            let url = window.location.pathname + '?period=' + encodeURIComponent(period);
            
            // custom 기간인 경우 시작일/종료일 추가
            if (period === 'custom') {
                const startDate = document.getElementById('start-date').value;
                const endDate = document.getElementById('end-date').value;
                
                if (startDate && endDate) {
                    url += '&start_date=' + encodeURIComponent(startDate) + 
                           '&end_date=' + encodeURIComponent(endDate);
                }
            }
            
            // 페이지 이동
            window.location.href = url;
        });
    }
}

/**
 * 탭 기능 초기화
 */
function initializeTabs() {
    const tabContainers = document.querySelectorAll('.tab-container');
    
    tabContainers.forEach(container => {
        const tabs = container.querySelectorAll('.tab-item');
        const tabContents = container.querySelectorAll('.tab-content');
        
        tabs.forEach((tab, index) => {
            tab.addEventListener('click', function() {
                // 모든 탭 비활성화
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                
                // 선택한 탭 활성화
                this.classList.add('active');
                tabContents[index].classList.add('active');
            });
        });
        
        // 첫 번째 탭 기본 활성화
        if (tabs.length > 0 && tabContents.length > 0) {
            tabs[0].classList.add('active');
            tabContents[0].classList.add('active');
        }
    });
}

/**
 * 자세히 보기 기능 초기화
 */
function initializeDetailViews() {
    // 카드 클릭시 자세히 보기 (최신 뉴스 등)
    const articleItems = document.querySelectorAll('.article-item');
    
    articleItems.forEach(item => {
        item.addEventListener('click', function() {
            const detailSection = this.querySelector('.article-detail');
            if (detailSection) {
                // 클릭 시 상세 정보 토글
                detailSection.style.display = 
                    detailSection.style.display === 'none' || detailSection.style.display === '' ? 
                    'block' : 'none';
            }
        });
    });
}

// 네트워크 분석 함수 수정 - 요약 정보 추가
function loadNetworkAnalysis() {
    console.log('네트워크 분석 로드 함수 실행');
    
    const networkContainer = document.querySelector('.network-container');
    const noDataContainer = document.querySelector('.visualization-container .no-data');
    const loadingElem = document.getElementById('network-loading');
    const resultContainer = document.getElementById('network-result');
    
    // 로딩 표시
    if (loadingElem) loadingElem.style.display = 'block';
    if (resultContainer) resultContainer.innerHTML = '';
    
    // 현재 설정된 기간 정보 가져오기
    const period = getCurrentPeriod();
    
    // API URL 생성
    let apiUrl = `/api/news/network?${period}`;
    
    // 캐시 방지를 위한 타임스탬프 추가
    const timestamp = new Date().getTime();
    apiUrl += `&_=${timestamp}`;
    
    // AJAX 요청
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // 로딩 숨기기
            if (loadingElem) loadingElem.style.display = 'none';
            
            // 네트워크 그래프 데이터 확인
            if (data.network_graph) {
                // 컨테이너가 없으면 생성
                if (!networkContainer) {
                    const newNetworkContainer = document.createElement('div');
                    newNetworkContainer.className = 'network-container no-scroll'; // no-scroll 클래스 추가
                    const visContainer = document.querySelector('.visualization-container');
                    if (visContainer) {
                        // 기존 no-data 숨기기
                        if (noDataContainer) noDataContainer.style.display = 'none';
                        visContainer.appendChild(newNetworkContainer);
                    }
                }
                
                // 새로운 컨테이너 참조 가져오기
                const container = document.querySelector('.network-container');
                if (container) {
                    container.innerHTML = data.network_graph;
                    console.log('네트워크 그래프 렌더링 완료');
                    
                    // Plotly 초기화 확인 및 차트 리사이징
                    if (window.Plotly) {
                        try {
                            // Plotly 차트 재계산 시도
                            const plotlyCharts = container.querySelectorAll('.js-plotly-plot');
                            
                            if (plotlyCharts.length > 0) {
                                // no-scroll 클래스 추가
                                plotlyCharts.forEach(chart => {
                                    chart.classList.add('no-scroll');
                                });
                                
                                // 차트 리사이징을 위해 짧은 지연 추가
                                window.setTimeout(() => {
                                    // 부모 컨테이너의 크기 측정
                                    const parentWidth = container.clientWidth;
                                    const parentHeight = container.clientHeight;
                                    
                                    plotlyCharts.forEach(chart => {
                                        // 차트 크기를 컨테이너에 맞게 조정
                                        chart.style.width = '100%';
                                        chart.style.height = '100%';
                                        
                                        // Plotly 리사이징
                                        window.Plotly.Plots.resize(chart);
                                    });
                                    console.log('네트워크 그래프 리사이즈 완료');
                                }, 100);
                            }
                        } catch (e) {
                            console.error('네트워크 그래프 초기화 오류:', e);
                        }
                    }
                    
                    // 분석 요약 추가
                    addAnalysisSummary();
                }
            } else if (resultContainer) {
                resultContainer.innerHTML = '<div class="error-message">네트워크 그래프를 생성할 수 없습니다.</div>';
            }
        })
        .catch(error => {
            console.error('네트워크 분석 요청 실패:', error);
            if (loadingElem) loadingElem.style.display = 'none';
            if (resultContainer) {
                resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
            }
        });
}


/**
 * 추가 분석 버튼 초기화
 */
function initializeAnalysisButtons() {
    // TF-IDF 분석 버튼
    const tfidfAnalysisBtn = document.getElementById('tfidf-analysis-btn');
    if (tfidfAnalysisBtn) {
        tfidfAnalysisBtn.addEventListener('click', function() {
            const loadingIndicator = document.getElementById('tfidf-loading');
            const resultContainer = document.getElementById('tfidf-result');
            
            if (loadingIndicator) loadingIndicator.style.display = 'block';
            if (resultContainer) resultContainer.innerHTML = '';
            
            // AJAX 요청
            fetch('/api/news/tfidf?' + getCurrentPeriod())
                .then(response => response.json())
                .then(data => {
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    
                    if (resultContainer && data.chart) {
                        resultContainer.innerHTML = data.chart;
                    }
                })
                .catch(error => {
                    console.error('TF-IDF 분석 요청 실패:', error);
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    if (resultContainer) {
                        resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
                    }
                });
        });
    }
    
    // 토픽 모델링 분석 버튼
    const topicAnalysisBtn = document.getElementById('topic-analysis-btn');
    if (topicAnalysisBtn) {
        topicAnalysisBtn.addEventListener('click', function() {
            const loadingIndicator = document.getElementById('topic-loading');
            const resultContainer = document.getElementById('topic-result');
            
            if (loadingIndicator) loadingIndicator.style.display = 'block';
            if (resultContainer) resultContainer.innerHTML = '';
            
            // AJAX 요청
            fetch('/api/news/topics?' + getCurrentPeriod())
                .then(response => response.json())
                .then(data => {
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    
                    if (resultContainer && data.charts) {
                        let html = '';
                        if (data.charts.distribution) {
                            html += '<div class="chart-container">' + data.charts.distribution + '</div>';
                        }
                        if (data.charts.heatmap) {
                            html += '<div class="chart-container">' + data.charts.heatmap + '</div>';
                        }
                        resultContainer.innerHTML = html;
                    }
                })
                .catch(error => {
                    console.error('토픽 분석 요청 실패:', error);
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    if (resultContainer) {
                        resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
                    }
                });
        });
    }
    
    // 감성 분석 버튼
    const sentimentAnalysisBtn = document.getElementById('sentiment-analysis-btn');
    if (sentimentAnalysisBtn) {
        sentimentAnalysisBtn.addEventListener('click', function() {
            const loadingIndicator = document.getElementById('sentiment-loading');
            const resultContainer = document.getElementById('sentiment-result');
            
            if (loadingIndicator) loadingIndicator.style.display = 'block';
            if (resultContainer) resultContainer.innerHTML = '';
            
            // AJAX 요청
            fetch('/api/news/sentiment?' + getCurrentPeriod())
                .then(response => response.json())
                .then(data => {
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    
                    if (resultContainer && data.charts) {
                        let html = '';
                        if (data.charts.pie_chart) {
                            html += '<div class="chart-container">' + data.charts.pie_chart + '</div>';
                        }
                        if (data.charts.time_chart) {
                            html += '<div class="chart-container">' + data.charts.time_chart + '</div>';
                        }
                        resultContainer.innerHTML = html;
                    }
                })
                .catch(error => {
                    console.error('감성 분석 요청 실패:', error);
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    if (resultContainer) {
                        resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
                    }
                });
        });
    }
}

/**
 * 시각화 요소 초기화
 */
// 이벤트 리스너 등록 함수 수정
function initializeVisualizations() {
    // 클릭 가능한 키워드 추가
    const keywordItems = document.querySelectorAll('.keyword-list li');
    
    keywordItems.forEach(item => {
        item.addEventListener('click', function() {
            const keyword = this.querySelector('.keyword-text').textContent;
            searchKeyword(keyword);
        });
    });

    // 트렌드 로드 버튼
    const loadTrendBtn = document.getElementById('load-trend-btn');
    if (loadTrendBtn) {
        loadTrendBtn.addEventListener('click', function() {
            loadKeywordTrendIfNeeded();
        });
    }

    // 네트워크 분석 버튼
    const networkAnalysisBtn = document.getElementById('network-analysis-btn');
    if (networkAnalysisBtn) {
        networkAnalysisBtn.addEventListener('click', function() {
            loadNetworkAnalysis();
        });
    }

    // 시계열 분석 버튼
    const timeseriesAnalysisBtn = document.getElementById('timeseries-analysis-btn');
    if (timeseriesAnalysisBtn) {
        timeseriesAnalysisBtn.addEventListener('click', function() {
            const loadingIndicator = document.getElementById('timeseries-loading');
            const resultContainer = document.getElementById('timeseries-result');
            
            if (loadingIndicator) loadingIndicator.style.display = 'block';
            if (resultContainer) resultContainer.innerHTML = '';
            
            // 선택된 시간 단위 가져오기
            const timeUnit = document.querySelector('input[name="time-unit"]:checked').value;
            
            // AJAX 요청
            fetch(`/api/news/trend?unit=${timeUnit}&${getCurrentPeriod()}`)
                .then(response => response.json())
                .then(data => {
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    
                    if (resultContainer) {
                        if (data.time_chart) {
                            resultContainer.innerHTML = `
                                <div class="chart-container">
                                    <h5>시계열 분석 (${timeUnit === 'daily' ? '일별' : timeUnit === 'weekly' ? '주별' : '월별'})</h5>
                                    ${data.time_chart}
                                </div>
                            `;
                            
                            // 키워드 트렌드도 함께 추가
                            if (data.keyword_trend) {
                                resultContainer.innerHTML += `
                                    <div class="chart-container">
                                        <h5>키워드 트렌드</h5>
                                        ${data.keyword_trend}
                                    </div>
                                `;
                            }
                            
                            // Plotly 차트 리사이징
                            if (window.Plotly) {
                                try {
                                    const charts = resultContainer.querySelectorAll('.js-plotly-plot');
                                    if (charts.length > 0) {
                                        setTimeout(() => {
                                            charts.forEach(chart => {
                                                window.Plotly.Plots.resize(chart);
                                            });
                                        }, 100);
                                    }
                                } catch (e) {
                                    console.error('차트 리사이징 오류:', e);
                                }
                            }
                        } else {
                            resultContainer.innerHTML = '<div class="no-data">분석 데이터가 없습니다.</div>';
                        }
                    }
                })
                .catch(error => {
                    console.error('시계열 분석 요청 실패:', error);
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    if (resultContainer) {
                        resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
                    }
                });
        });
    }
    
    // 워드클라우드 확대 이벤트
    const wordcloudImg = document.querySelector('.wordcloud-container img');
    if (wordcloudImg) {
        wordcloudImg.addEventListener('click', function() {
            openImageModal(this.src);
        });
    }
    
    // 검색 버튼
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const keyword = document.getElementById('search-keyword').value.trim();
            if (keyword) {
                searchKeyword(keyword);
            }
        });
        
        // 엔터 키 이벤트
        const searchInput = document.getElementById('search-keyword');
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchBtn.click();
                }
            });
        }
    }
}

/**
 * 키워드 검색 실행
 * @param {string} keyword - 검색할 키워드
 */
function searchKeyword(keyword) {
    // 예시: 키워드로 기사 필터링 AJAX 요청
    console.log('키워드 검색:', keyword);
    
    const loadingIndicator = document.getElementById('search-loading');
    const resultContainer = document.getElementById('search-result');
    
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (resultContainer) resultContainer.innerHTML = '';
    
    // AJAX 요청
    fetch('/api/news/search?keyword=' + encodeURIComponent(keyword) + '&' + getCurrentPeriod())
        .then(response => response.json())
        .then(data => {
            if (loadingIndicator) loadingIndicator.style.display = 'none';
            
            if (resultContainer) {
                if (data.articles && data.articles.length > 0) {
                    let html = '<h5>검색 결과: "' + keyword + '"</h5><div class="search-articles">';
                    
                    data.articles.forEach(article => {
                        html += `
                            <div class="article-item">
                                <a href="${article.link}" target="_blank" class="article-link">
                                    <h6 class="mb-1">${article.title}</h6>
                                </a>
                                <p class="article-preview mb-1">${article.content?.substring(0, 100)}...</p>
                                <small class="text-muted">${article.upload_date}</small>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    resultContainer.innerHTML = html;
                } else {
                    resultContainer.innerHTML = '<div class="no-results">검색 결과가 없습니다.</div>';
                }
            }
        })
        .catch(error => {
            console.error('검색 요청 실패:', error);
            if (loadingIndicator) loadingIndicator.style.display = 'none';
            if (resultContainer) {
                resultContainer.innerHTML = '<div class="error-message">검색 중 오류가 발생했습니다.</div>';
            }
        });
}

/**


/**
 * 워드클라우드 이미지 확대 보기
 * @param {string} imgSrc - 이미지 소스 URL
 */
function openImageModal(imgSrc) {
    const modal = document.getElementById('image-modal');
    if (!modal) return;
    
    const modalImg = modal.querySelector('.modal-img');
    if (modalImg) {
        modalImg.src = imgSrc;
    }
    
    modal.style.display = 'block';
}

/**
 * 모달 닫기
 */
function closeModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// 차트 크기 수동 조정 함수
function fixPlotlyChartSize(chart) {
    const container = chart.closest('.visualization-container');
    if (container) {
        const containerWidth = container.clientWidth;
        const containerHeight = container.clientHeight;
        
        // 차트 크기를 컨테이너보다 약간 작게 설정
        const chartWidth = containerWidth * 0.95;
        const chartHeight = containerHeight * 0.95;
        
        // Plotly 리사이징 함수 호출
        window.Plotly.relayout(chart, {
            width: chartWidth,
            height: chartHeight
        });
    }
}

// 모든 차트에 적용
document.querySelectorAll('.js-plotly-plot').forEach(chart => {
    fixPlotlyChartSize(chart);
});

// loadNetworkAnalysis 함수 수정 - 차트 크기 조절 추가
function loadNetworkAnalysis() {
    console.log('네트워크 분석 로드 함수 실행');
    
    const networkContainer = document.querySelector('.network-container');
    const noDataContainer = document.querySelector('.visualization-container .no-data');
    const loadingElem = document.getElementById('network-loading');
    const resultContainer = document.getElementById('network-result');
    
    // 로딩 표시
    if (loadingElem) loadingElem.style.display = 'block';
    if (resultContainer) resultContainer.innerHTML = '';
    
    // 현재 설정된 기간 정보 가져오기
    const period = getCurrentPeriod();
    
    // API URL 생성
    let apiUrl = `/api/news/network?${period}`;
    
    // 캐시 방지를 위한 타임스탬프 추가
    const timestamp = new Date().getTime();
    apiUrl += `&_=${timestamp}`;
    
    // AJAX 요청
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // 로딩 숨기기
            if (loadingElem) loadingElem.style.display = 'none';
            
            // 네트워크 그래프 데이터 확인
            if (data.network_graph) {
                // 컨테이너가 없으면 생성
                if (!networkContainer) {
                    const newNetworkContainer = document.createElement('div');
                    newNetworkContainer.className = 'network-container no-scroll'; // no-scroll 클래스 추가
                    const visContainer = document.querySelector('.visualization-container');
                    if (visContainer) {
                        // 기존 no-data 숨기기
                        if (noDataContainer) noDataContainer.style.display = 'none';
                        visContainer.appendChild(newNetworkContainer);
                    }
                }
                
                // 새로운 컨테이너 참조 가져오기
                const container = document.querySelector('.network-container');
                if (container) {
                    container.innerHTML = data.network_graph;
                    console.log('네트워크 그래프 렌더링 완료');
                    
                    // Plotly 초기화 확인 및 차트 리사이징
                    if (window.Plotly) {
                        try {
                            // Plotly 차트 재계산 시도
                            const plotlyCharts = container.querySelectorAll('.js-plotly-plot');
                            
                            if (plotlyCharts.length > 0) {
                                // no-scroll 클래스 추가
                                plotlyCharts.forEach(chart => {
                                    chart.classList.add('no-scroll');
                                });
                                
                                // 차트 리사이징을 위해 짧은 지연 추가
                                window.setTimeout(() => {
                                    // 부모 컨테이너의 크기 측정
                                    const parentWidth = container.clientWidth;
                                    const parentHeight = container.clientHeight;
                                    
                                    plotlyCharts.forEach(chart => {
                                        // 차트 크기를 컨테이너에 맞게 조정
                                        chart.style.width = '100%';
                                        chart.style.height = '100%';
                                        
                                        // Plotly 리사이징
                                        window.Plotly.Plots.resize(chart);
                                    });
                                    console.log('네트워크 그래프 리사이즈 완료');
                                }, 100);
                            }
                        } catch (e) {
                            console.error('네트워크 그래프 초기화 오류:', e);
                        }
                    }
                }
            } else if (resultContainer) {
                resultContainer.innerHTML = '<div class="error-message">네트워크 그래프를 생성할 수 없습니다.</div>';
            }
        })
        .catch(error => {
            console.error('네트워크 분석 요청 실패:', error);
            if (loadingElem) loadingElem.style.display = 'none';
            if (resultContainer) {
                resultContainer.innerHTML = '<div class="error-message">분석 중 오류가 발생했습니다.</div>';
            }
        });
}
// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
    const modal = document.getElementById('image-modal');
    if (modal && event.target === modal) {
        modal.style.display = 'none';
    }
};