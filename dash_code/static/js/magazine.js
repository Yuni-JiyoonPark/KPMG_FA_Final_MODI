/**
 * 매거진 페이지 JavaScript
 */

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
    const wordcloudContainer = document.querySelector('.plotly-chart-container');
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
                    TF-IDF 분석 결과, '결과', '트렌드', '연출', '화이트', '디자인' 등의 키워드가 주요하게 도출되었습니다. 특히 '결과'와 '트렌드' 관련 언급이 두드러지며, 패션 산업 트렌드가 주요 화제로 떠오르고 있습니다. 컬러와 디자인에 관한 키워드가 많이 등장하며, 최근 패션 업계가 다양한 스타일과 연출 방식에 초점을 맞추고 있음을 시사합니다.
                </p>
            </div>
        `;
        wordcloudContainer.parentElement.appendChild(wordcloudSummary);
    }

    // 네트워크 분석 요약 추가
    const networkContainer = document.querySelector('.plotly-chart-container');
    if (networkContainer && !networkContainer.parentElement.querySelector('.analysis-summary')) {
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
                    연관어 네트워크 분석 결과, '트렌드', '스타일링', '패션', '홀리데이', '블랙' 등의 키워드가 중심 노드로 강한 연결성을 보이고 있습니다. 특히 '트렌드'와 '스타일링' 노드의 연결 강도가 높아, 현재 패션 트렌드와 스타일링 방식이 주요 관심사임을 알 수 있습니다. 컬러와 관련된 '블랙'과 계절 테마인 '홀리데이' 키워드가 중요하게 나타나며, 최신 트렌드가 계절적 요소와 기본 컬러를 중심으로 형성되고 있음을 시사합니다.
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

document.addEventListener('DOMContentLoaded', function() {
    // 폰트 어썸 스크립트 추가
    if (!document.querySelector('link[href*="font-awesome"]') && !document.querySelector('link[href*="fontawesome"]')) {
        const fontAwesomeLink = document.createElement('link');
        fontAwesomeLink.rel = 'stylesheet';
        fontAwesomeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
        document.head.appendChild(fontAwesomeLink);
    }

     // 기존 요약 토글 기능 초기화
     initializeSummaryToggles();
    
     // 새로운 요약 추가
     addAnalysisSummary();
     
    // 매거진 필터 기능
    const filterTags = document.querySelectorAll('.filter-tag');
    
    // URL에서 현재 선택된 매거진 가져오기
    const params = new URLSearchParams(window.location.search);
    let currentMagazines = params.getAll('magazine');
    
    // 기본 매거진 리스트
    const defaultMagazines = ['jentestore', 'marieclaire', 'vogue', 'wkorea', 'wwdkorea'];
    
    // 선택된 매거진이 없으면 기본값 설정
    if (currentMagazines.length === 0) {
        currentMagazines = defaultMagazines;
        
        // URL 매개변수 설정
        defaultMagazines.forEach(magazine => {
            params.append('magazine', magazine);
        });
        
        // URL 업데이트 및 페이지 새로고침
        window.location.href = `${window.location.pathname}?${params.toString()}`;
        return;
    }
    
    // 필터 태그 클릭 이벤트
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const magazineName = this.getAttribute('data-magazine');
            const isActive = this.classList.contains('active');
            
            console.log(`매거진 클릭: ${magazineName}, 현재 상태: ${isActive ? '활성' : '비활성'}`); // 디버깅용
            
            // URL 업데이트를 위한 현재 매개변수
            const params = new URLSearchParams(window.location.search);
            let currentMagazines = params.getAll('magazine');
            
            // currentMagazines가 비어있으면 기본 매거진 리스트로 초기화
            if (currentMagazines.length === 0) {
                currentMagazines = defaultMagazines;
            }
            
            if (isActive) {
                // 선택 해제 시 최소 하나의 매거진은 선택되어 있어야 함
                if (currentMagazines.length > 1) {
                    const index = currentMagazines.indexOf(magazineName);
                    if (index > -1) {
                        currentMagazines.splice(index, 1);
                        this.classList.remove('active');
                    }
                } else {
                    console.log('최소 하나의 매거진은 선택되어 있어야 합니다.'); // 디버깅용
                    return; // 선택 해제하지 않고 종료
                }
            } else {
                // 선택 추가
                if (!currentMagazines.includes(magazineName)) {
                    currentMagazines.push(magazineName);
                    this.classList.add('active');
                }
            }
            
            console.log('선택된 매거진:', currentMagazines); // 디버깅용
            
            // URL 매개변수 설정
            params.delete('magazine');
            currentMagazines.forEach(magazine => {
                params.append('magazine', magazine);
            });
            
            // 기간 설정 유지
            const periodSelect = document.getElementById('period-select');
            if (periodSelect && periodSelect.value) {
                params.set('period', periodSelect.value);
            } else {
                // 현재 URL에서 period 값을 가져와서 유지
                const currentPeriod = params.get('period');
                if (currentPeriod) {
                    params.set('period', currentPeriod);
                }
            }
            
            // 사용자 정의 날짜 범위 유지
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            if (startDateInput && endDateInput && startDateInput.value && endDateInput.value) {
                params.set('start_date', startDateInput.value);
                params.set('end_date', endDateInput.value);
            } else {
                // 현재 URL에서 날짜 값을 가져와서 유지
                const currentStartDate = params.get('start_date');
                const currentEndDate = params.get('end_date');
                if (currentStartDate && currentEndDate) {
                    params.set('start_date', currentStartDate);
                    params.set('end_date', currentEndDate);
                }
            }
            
            // URL 업데이트 및 페이지 새로고침
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    });
    
    // 카드뉴스 필터 기능
    const filterButtons = document.querySelectorAll('.magazine-filter-btn');
    const magazineCards = document.querySelectorAll('.magazine-card');
    
    // 디버깅 로깅 함수
    const logDebug = (message) => {
        console.log(`[CARD_NEWS] ${message}`);
    };
    
    // 필터링 결과 카운트 표시 기능
    const updateFilteringResults = (count) => {
        const cardGrid = document.querySelector('.magazine-card-grid');
        if (!cardGrid) {
            logDebug('카드 그리드를 찾을 수 없습니다.');
            return;
        }
        
        const existingInfo = cardGrid.querySelector('.filtering-info');
        
        if (existingInfo) {
            cardGrid.removeChild(existingInfo);
        }
        
        if (count === 0) {
            const infoElement = document.createElement('div');
            infoElement.className = 'filtering-info no-data';
            infoElement.textContent = '선택한 매거진의 카드뉴스가 없습니다.';
            cardGrid.appendChild(infoElement);
        }
    };
    
    // 매거진 필터 초기화 함수
    function initMagazineFilter() {
        const filterButtons = document.querySelectorAll('.magazine-filter-btn');
        const magazineCards = document.querySelectorAll('.magazine-card');
        
        // URL에서 현재 선택된 매거진 가져오기
        const urlParams = new URLSearchParams(window.location.search);
        const selectedMagazines = urlParams.getAll('magazine');
        console.log('[CARD_NEWS] URL 매거진 파라미터:', selectedMagazines);
        
        // 기본 필터 적용
        if (selectedMagazines.length > 0) {
            // 선택된 매거진이 있으면 해당 매거진 필터 적용
            filterCards(selectedMagazines[0]);
            
            // 해당 버튼 활성화
            filterButtons.forEach(btn => {
                const magazine = btn.getAttribute('data-magazine');
                btn.classList.toggle('active', magazine === selectedMagazines[0]);
            });
        } else {
            // 선택된 매거진이 없으면 '전체' 필터 적용
            filterCards('all');
            
            // '전체' 버튼 활성화
            filterButtons.forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-magazine') === 'all');
            });
        }
        
        // 필터 버튼 클릭 이벤트
        filterButtons.forEach(button => {
            // 기존 이벤트 리스너 제거
            button.removeEventListener('click', handleFilterButtonClick);
            // 새 이벤트 리스너 등록
            button.addEventListener('click', handleFilterButtonClick);
        });
    }
    
    // 필터 버튼 클릭 핸들러
    function handleFilterButtonClick() {
        const magazine = this.getAttribute('data-magazine');
        console.log('[CARD_NEWS] 필터 버튼 클릭:', magazine);
        
        // 현재 URL 파라미터 가져오기
        const params = new URLSearchParams(window.location.search);
        
        // 매거진 파라미터 업데이트
        if (magazine === 'all') {
            params.delete('magazine');
        } else {
            params.set('magazine', magazine);
        }
        
        // 기존 기간 설정 유지
        const periodSelect = document.getElementById('period-select');
        if (periodSelect && periodSelect.value) {
            params.set('period', periodSelect.value);
        }
        
        // 사용자 정의 날짜 범위 유지
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        if (startDateInput && endDateInput && startDateInput.value && endDateInput.value) {
            params.set('start_date', startDateInput.value);
            params.set('end_date', endDateInput.value);
        }
        
        // URL 업데이트 및 페이지 새로고침
        window.location.search = params.toString();
    }
    
    // 카드 필터링 함수
    function filterCards(selectedMagazine) {
        console.log('[CARD_NEWS] 필터링 시작:', selectedMagazine);
        
        const cards = document.querySelectorAll('.magazine-card');
        let visibleCount = 0;
        const magazineCounts = {};
        
        cards.forEach(card => {
            const cardMagazine = card.getAttribute('data-magazine')?.toLowerCase();
            if (!cardMagazine) {
                console.warn('[CARD_NEWS] data-magazine 속성이 없는 카드 발견');
                return;
            }
            
            console.log('[CARD_NEWS] 카드 확인:', {
                magazine: cardMagazine,
                title: card.querySelector('.magazine-card-title')?.textContent
            });
            
            // magazineCounts 업데이트
            magazineCounts[cardMagazine] = (magazineCounts[cardMagazine] || 0) + 1;
            
            const shouldShow = selectedMagazine === 'all' || cardMagazine === selectedMagazine.toLowerCase();
            card.style.display = shouldShow ? 'block' : 'none';
            if (shouldShow) visibleCount++;
        });
        
        console.log('[CARD_NEWS] 필터링 결과:', {
            selectedMagazine,
            visibleCount,
            magazineCounts
        });
        
        // 결과가 없을 경우 메시지 표시
        updateNoDataMessage(visibleCount);
    }
    
    // 결과 없음 메시지 업데이트
    function updateNoDataMessage(visibleCount) {
        const cardGrid = document.querySelector('.magazine-card-grid');
        let noDataMessage = document.querySelector('.no-data');
        
        if (visibleCount === 0) {
            if (!noDataMessage) {
                noDataMessage = document.createElement('div');
                noDataMessage.className = 'no-data';
                noDataMessage.textContent = '선택한 매거진의 카드뉴스가 없습니다.';
                cardGrid.appendChild(noDataMessage);
            }
        } else if (noDataMessage) {
            noDataMessage.remove();
        }
    }
    
    // 페이지 로드 시 초기화
    initMagazineFilter();
    
    // 동적 콘텐츠 로드 후 재초기화
    window.addEventListener('load', function() {
        setTimeout(initMagazineFilter, 300);
    });
    
    // 키워드 클릭 시 하이라이트 기능
    const keywordItems = document.querySelectorAll('.keyword-item');
    keywordItems.forEach(item => {
        item.addEventListener('click', function() {
            const keyword = this.querySelector('.keyword-text').textContent.trim();
            highlightKeyword(keyword);
        });
    });
    
    // 키워드 하이라이트 함수
    function highlightKeyword(keyword) {
        // 모든 키워드 항목 순회
        keywordItems.forEach(item => {
            const text = item.querySelector('.keyword-text').textContent.trim();
            if (text === keyword) {
                item.classList.add('highlighted');
            } else {
                item.classList.remove('highlighted');
            }
        });
        
        // 공통 키워드 태그도 하이라이트
        const commonTags = document.querySelectorAll('.common-keyword-tag');
        commonTags.forEach(tag => {
            if (tag.textContent.trim() === keyword) {
                tag.classList.add('highlighted');
            } else {
                tag.classList.remove('highlighted');
            }
        });
    }
    
    // 키워드 탭 전환 기능 개선
    const keywordTabs = document.querySelectorAll('.keyword-tab');
    const keywordChartContainers = document.querySelectorAll('.keyword-charts-container');
    
    keywordTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // 현재 탭 키워드 가져오기
            const keyword = this.getAttribute('data-keyword');
            console.log(`키워드 탭 선택: ${keyword}`);
            
            // 활성 탭 업데이트
            keywordTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // 차트 컨테이너 표시/숨김 처리
            keywordChartContainers.forEach(container => {
                const containerId = container.id;
                const containerKeyword = containerId.replace('charts-', '');
                
                if (containerKeyword === keyword) {
                    container.style.display = 'block';
                    
                    // 해당 컨테이너의 Plotly 차트 찾기
                    const plotlyCharts = container.querySelectorAll('.js-plotly-plot');
                    
                    if (plotlyCharts.length > 0 && window.Plotly) {
                        console.log(`${keyword} 탭의 Plotly 차트 리사이징`);
                        
                        // 약간의 지연 후 리사이징 실행 (렌더링 완료 확보)
                        setTimeout(() => {
                            plotlyCharts.forEach(chart => {
                                try {
                                    // 파이차트 컨테이너 찾기
                                    const pieChartContainer = chart.closest('.pie-chart-container');
                                    
                                    if (pieChartContainer) {
                                        // 컨테이너 크기 측정
                                        const containerWidth = pieChartContainer.clientWidth;
                                        
                                        // 차트 크기 설정 (가로세로 비율 1:1 유지)
                                        const chartSize = Math.min(containerWidth, 350);
                                        
                                        // Plotly 차트 리사이징
                                        window.Plotly.relayout(chart, {
                                            width: chartSize,
                                            height: chartSize,
                                            autosize: false
                                        });
                                        
                                        console.log(`${keyword} 탭의 차트 크기 조정 완료: ${chartSize}x${chartSize}`);
                                    }
                                } catch (e) {
                                    console.error(`차트 리사이징 오류:`, e);
                                }
                            });
                        }, 50);
                    }
                } else {
                    container.style.display = 'none';
                }
            });
        });
    });

    // 창 크기 변경 시 활성 탭의 차트 리사이징
    window.addEventListener('resize', function() {
        // 현재 활성화된 탭 찾기
        const activeTab = document.querySelector('.keyword-tab.active');
        if (activeTab) {
            // 리사이징 트리거
            activeTab.click();
        }
    });
    
    // 페이지 로드 후 첫 번째 탭 클릭 이벤트 트리거 (기본 탭 설정)
    setTimeout(() => {
        const firstTab = document.querySelector('.keyword-tab');
        if (firstTab) {
            firstTab.click();
        }
    }, 200);
    
    // 카테고리 데이터 로드 및 차트 초기화
    if (document.getElementById('category-count-chart')) {
        // Plotly.js 스크립트 로드 확인
        if (typeof Plotly === 'undefined') {
            // Plotly.js가 없으면 동적으로 로드
            const script = document.createElement('script');
            script.src = 'https://cdn.plot.ly/plotly-latest.min.js';
            script.onload = function() {
                loadCategoryData('item');
            };
            document.head.appendChild(script);
        } else {
            loadCategoryData('item');
        }
        
        // 라디오 버튼 이벤트 리스너
        const radioButtons = document.querySelectorAll('input[name="category-type"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    loadCategoryData(this.value);
                }
            });
        });
    }

    // 기간 선택 변경 시 카테고리 차트 갱신
    const periodSelect = document.getElementById('period-select');
    if (periodSelect) {
        periodSelect.addEventListener('change', function() {
            // 현재 표시 중인 기간 업데이트
            const periodDisplay = document.querySelector('.period-display span');
            if (periodDisplay) {
                periodDisplay.textContent = this.options[this.selectedIndex].text;
            }
            
            // 현재 선택된 카테고리 타입 확인
            const selectedType = document.querySelector('input[name="category-type"]:checked');
            if (selectedType) {
                // 약간의 지연 후 카테고리 데이터 다시 로드
                setTimeout(() => {
                    loadCategoryData(selectedType.value);
                }, 300);
            }
        });
    }
    
    // 직접 설정 날짜 적용 버튼 클릭 시 차트 갱신
    const applyDateBtn = document.querySelector('.apply-date-btn');
    if (applyDateBtn) {
        applyDateBtn.addEventListener('click', function() {
            // 적용 후 카테고리 차트 갱신 (약간의 지연 추가)
            setTimeout(() => {
                const selectedType = document.querySelector('input[name="category-type"]:checked');
                if (selectedType) {
                    loadCategoryData(selectedType.value);
                }
                
                // 현재 표시 중인 기간 업데이트
                const periodDisplay = document.querySelector('.period-display span');
                if (periodDisplay) {
                    const startDate = document.querySelector('#start-date').value;
                    const endDate = document.querySelector('#end-date').value;
                    periodDisplay.textContent = `${startDate} ~ ${endDate}`;
                }
            }, 500);
        });
    }
});

// 카테고리별 데이터 로드 및 차트 생성 함수
function loadCategoryData(categoryType = 'item') {
    // 로딩 표시
    document.getElementById('category-loading').style.display = 'flex';
    document.getElementById('category-count-chart').innerHTML = '';
    document.getElementById('category-growth-chart').innerHTML = '';
    
    // 카테고리 제목 업데이트
    const categoryTitles = {
        'item': '아이템',
        'color': '컬러',
        'material': '소재',
        'print': '프린트',
        'style': '스타일'
    };
    
    // 현재 URL의 쿼리 파라미터에서 기간 값 가져오기
    const urlParams = new URLSearchParams(window.location.search);
    const currentPeriod = urlParams.get('period') || '7일';
    const startDate = urlParams.get('start_date');
    const endDate = urlParams.get('end_date');
    
    console.log("현재 기간 설정값:", currentPeriod, startDate, endDate); // 디버깅용
    
    // API 호출 URL 구성
    let apiUrl = `/api/category-data?type=${categoryType}&period=${currentPeriod}`;
    
    // custom 기간인 경우 시작일/종료일 추가
    if (currentPeriod === 'custom' && startDate && endDate) {
        apiUrl += `&start_date=${startDate}&end_date=${endDate}`;
    }
    
    console.log("카테고리 데이터 요청 URL:", apiUrl); // 디버깅용
    
    // 데이터 가져오기
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // 로딩 표시 숨기기
            document.getElementById('category-loading').style.display = 'none';
            
            if (data.error) {
                document.getElementById('category-count-chart').innerHTML = `<div class="error">${data.error}</div>`;
                document.getElementById('category-growth-chart').innerHTML = `<div class="error">${data.error}</div>`;
                return;
            }
            
            if (!data.categories || data.categories.length === 0 || data.categories[0] === '데이터 없음') {
                document.getElementById('category-count-chart').innerHTML = '<div class="no-data">표시할 데이터가 없습니다.</div>';
                document.getElementById('category-growth-chart').innerHTML = '<div class="no-data">표시할 데이터가 없습니다.</div>';
                return;
            }
            
            // 카테고리 한글 이름 설정
            const categoryName = categoryTitles[categoryType] || categoryType;
            
            // 차트 생성 전 설정
            const config = {
                displayModeBar: false,
                responsive: true
            };
            
            // 차트 생성
            createCategoryCharts(data, categoryName, config);
        })
        .catch(error => {
            console.error('데이터 로드 중 오류 발생:', error);
            document.getElementById('category-loading').style.display = 'none';
            document.getElementById('category-count-chart').innerHTML = '<div class="error">데이터 로드 실패</div>';
            document.getElementById('category-growth-chart').innerHTML = '<div class="error">데이터 로드 실패</div>';
        });
}

// 카테고리 차트 생성
function createCategoryCharts(data, categoryName, config) {
    // 언급량 차트
    const countTrace = {
        x: data.categories,
        y: data.counts,
        type: 'bar',
        marker: {
            color: '#4a90e2'
        },
        name: '언급량'
    };
    
    const countLayout = {
        title: {
            text: `${categoryName} 카테고리별 언급량`,
            font: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                size: 16
            }
        },
        margin: { t: 40, r: 10, l: 60, b: 80 },
        height: 230,
        xaxis: {
            tickangle: -45,
            automargin: true,
            tickfont: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                size: 11
            }
        },
        yaxis: {
            title: {
                text: '언급량',
                font: {
                    family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                    size: 12
                }
            },
            automargin: true,
            tickfont: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif"
            }
        },
        showlegend: true,
        legend: {
            x: 0,
            y: 1.1,
            orientation: 'h'
        },
        font: {
            family: "'Noto Sans KR', 'Malgun Gothic', sans-serif"
        }
    };
    
    Plotly.newPlot('category-count-chart', [countTrace], countLayout, config);
    
    // 증감률 차트
    const growthTrace = {
        x: data.categories,
        y: data.growth_rates,
        type: 'bar',
        marker: {
            color: data.growth_rates.map(val => val >= 0 ? '#36D6BE' : '#FF5A5A')
        },
        name: '증감률(%)'
    };
    
    // 파레토 선 (상위 50% 표시)
    const categories = [...data.categories];
    const sortedIndexes = categories.map((_, i) => i)
        .sort((a, b) => data.counts[b] - data.counts[a]);
    
    let cumulativeSum = 0;
    const totalSum = data.counts.reduce((a, b) => a + b, 0);
    const pareto = [];
    
    for (let i = 0; i < sortedIndexes.length; i++) {
        cumulativeSum += data.counts[sortedIndexes[i]];
        pareto.push(cumulativeSum / totalSum * 100);
    }
    
    // 50% 라인 표시 (누적 데이터가 있는 경우만)
    let annotations = [];
    let shapes = [];
    
    if (totalSum > 0) {
        const fiftyPercentIndex = pareto.findIndex(val => val >= 50);
        if (fiftyPercentIndex > -1) {
            shapes.push({
                type: 'line',
                x0: categories[sortedIndexes[fiftyPercentIndex]],
                y0: -100,
                x1: categories[sortedIndexes[fiftyPercentIndex]],
                y1: 100,
                line: {
                    color: '#888888',
                    width: 1,
                    dash: 'dash'
                }
            });
            
            annotations.push({
                x: categories[sortedIndexes[fiftyPercentIndex]],
                y: Math.max(...data.growth_rates) * 0.8,
                xref: 'x',
                yref: 'y',
                text: `상위밀집 ${Math.round(pareto[fiftyPercentIndex])}%`,
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#888888',
                arrowsize: 1,
                arrowwidth: 1,
                ax: -40,
                ay: -40,
                bgcolor: 'rgba(255, 255, 255, 0.8)',
                bordercolor: '#888888',
                borderwidth: 1,
                borderpad: 4,
                font: {
                    family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                    size: 11
                }
            });
        }
    }
    
    const growthLayout = {
        title: {
            text: `${categoryName} 카테고리별 전기간 대비 증감률`,
            font: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                size: 16
            }
        },
        margin: { t: 40, r: 10, l: 60, b: 80 },
        height: 230,
        xaxis: {
            tickangle: -45,
            automargin: true,
            tickfont: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                size: 11
            }
        },
        yaxis: {
            title: {
                text: '증감률(%)',
                font: {
                    family: "'Noto Sans KR', 'Malgun Gothic', sans-serif",
                    size: 12
                }
            },
            automargin: true,
            zeroline: true,
            zerolinecolor: '#888888',
            zerolinewidth: 1,
            tickfont: {
                family: "'Noto Sans KR', 'Malgun Gothic', sans-serif"
            }
        },
        shapes: shapes,
        annotations: annotations,
        showlegend: true,
        legend: {
            x: 0,
            y: 1.1,
            orientation: 'h'
        },
        font: {
            family: "'Noto Sans KR', 'Malgun Gothic', sans-serif"
        }
    };
    
    Plotly.newPlot('category-growth-chart', [growthTrace], growthLayout, config);
}

// 페이지가 로드된 후 카테고리 데이터 초기화
window.addEventListener('load', function() {
    // URL 파라미터 변경 감지를 위한 이벤트 리스너
    let oldHref = window.location.href;
    
    // URL 변경을 감지하는 MutationObserver 활용
    const observer = new MutationObserver(function(mutations) {
        if (oldHref !== window.location.href) {
            oldHref = window.location.href;
            // URL이 변경되면 기간 표시 업데이트
            if (typeof updatePeriodDisplay === 'function') {
                updatePeriodDisplay();
            }
            
            // 현재 선택된 카테고리 타입으로 데이터 다시 로드
            const selectedType = document.querySelector('input[name="category-type"]:checked')?.value || 'item';
            if (document.getElementById('category-count-chart')) {
                loadCategoryData(selectedType);
            }
        }
    });
    
    observer.observe(document, { subtree: true, childList: true });
    
    // 기간 변경 이벤트를 위한 커스텀 이벤트 리스너
    document.addEventListener('periodChanged', function(e) {
        console.log('기간 변경 감지:', e.detail);
        
        // 카테고리 차트 있는 경우 데이터 다시 로드
        if (document.getElementById('category-count-chart')) {
            // 현재 선택된 카테고리 타입 확인
            const selectedType = document.querySelector('input[name="category-type"]:checked')?.value || 'item';
            // 약간의 지연 후 데이터 로드
            setTimeout(() => {
                loadCategoryData(selectedType);
                if (typeof updatePeriodDisplay === 'function') {
                    updatePeriodDisplay();
                }
            }, 300);
        }
    });
});