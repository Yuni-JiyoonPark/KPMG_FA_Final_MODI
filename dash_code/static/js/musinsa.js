
/**
 * 성별 탭 전환 기능 초기화 - 새로운 구조용
 */
function initGenderTabs() {
  const tabs = document.querySelectorAll('.gender-tab');
  
  if (!tabs || tabs.length === 0) {
    console.warn('성별 탭 요소를 찾을 수 없습니다.');
    return;
  }
  
  tabs.forEach(tab => {
    tab.addEventListener('click', function() {
      // 모든 탭에서 active 클래스 제거
      tabs.forEach(t => t.classList.remove('active'));
      
      // 클릭한 탭에 active 클래스 추가
      this.classList.add('active');
      
      // 모든 콘텐츠 숨기기
      const contents = document.querySelectorAll('.gender-content');
      contents.forEach(content => content.classList.remove('active'));
      
      // 선택한 탭의 콘텐츠 표시
      const tabId = this.getAttribute('data-tab');
      const targetContent = document.getElementById(tabId + '-tab');
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });
  
  console.log('성별 탭 초기화 완료');
}

// CSV 데이터 로드 및 차트 생성 초기화
document.addEventListener('DOMContentLoaded', function() {
  // 현재 페이지 ID 설정 및 기존 초기화 유지
  const pageId = 'musinsa';
  
  // 필터 초기화 (기존 period_filter.js 함수 호출)
  if (typeof initPeriodFilter === 'function') {
    initPeriodFilter(pageId);
  }
  
  // 탭 전환 기능 초기화
  initGenderTabs();
  
  // 브랜드 카드 클릭 이벤트 초기화
  initBrandCards();
  
  // 차트 초기화
  initCharts();
});

/**
 * 모든 차트 초기화 함수
 */
function initCharts() {
  // 로딩 표시
  showChartLoading('category-ratio-chart');
  showChartLoading('category-delta-chart');
  showChartLoading('price-range-chart');
  
  // CSV 데이터 로드
  loadMusinsaData()
    .then(data => {
      // 데이터 로드 성공시 차트 생성
      createCategoryRatioChart(data);
      createCategoryDeltaChart(data);
      createPriceRangeChart(data);
    })
    .catch(error => {
      console.error('데이터 로드 오류:', error);
      showChartError('category-ratio-chart', '데이터 로드 중 오류가 발생했습니다.');
      showChartError('category-delta-chart', '데이터 로드 중 오류가 발생했습니다.');
      showChartError('price-range-chart', '데이터 로드 중 오류가 발생했습니다.');
    });
}

/**
 * 무신사 CSV 데이터 로드 함수
 */
function loadMusinsaData() {
  return new Promise((resolve, reject) => {
    // 데이터 URL (현재 기간 기준)
    const period = document.querySelector('#period-select')?.value || '7일';
    const dataUrl = `/static/data/musinsa_data.csv`;
    
    // CSV 데이터 가져오기
    fetch(dataUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('데이터를 불러올 수 없습니다.');
        }
        return response.text();
      })
      .then(csvText => {
        // CSV 파싱 (Papaparse 사용)
        const parsed = Papa.parse(csvText, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true
        });
        
        if (parsed.errors && parsed.errors.length > 0) {
          console.warn('CSV 파싱 경고:', parsed.errors);
        }
        
        resolve(parsed.data);
      })
      .catch(error => {
        console.error('CSV 로드 오류:', error);
        reject(error);
      });
  });
}

/**
 * 차트 로딩 표시 함수
 */
function showChartLoading(chartId) {
  const chartElement = document.getElementById(chartId);
  if (chartElement) {
    // 기존 내용 제거
    chartElement.innerHTML = '';
    
    // 로딩 표시 추가
    const loadingElement = document.createElement('div');
    loadingElement.className = 'chart-loading';
    loadingElement.textContent = '차트 로딩 중';
    chartElement.appendChild(loadingElement);
  }
}

/**
 * 차트 오류 표시 함수
 */
function showChartError(chartId, errorMessage) {
  const chartElement = document.getElementById(chartId);
  if (chartElement) {
    // 기존 내용 제거
    chartElement.innerHTML = '';
    
    // 오류 메시지 표시
    const errorElement = document.createElement('div');
    errorElement.className = 'chart-error';
    errorElement.textContent = errorMessage;
    chartElement.appendChild(errorElement);
  }
}

/**
 * 카테고리별 비중 차트 생성 함수
 */
function createCategoryRatioChart(data) {
  // 카테고리별 집계
  const categoryCountMap = {};
  let totalCount = 0;
  
  // 데이터 집계
  data.forEach(item => {
    if (item.category) {
      categoryCountMap[item.category] = (categoryCountMap[item.category] || 0) + 1;
      totalCount++;
    }
  });
  
  // 비율 계산 및 정렬
  const categoryRatios = [];
  for (const category in categoryCountMap) {
    const count = categoryCountMap[category];
    const ratio = (count / totalCount) * 100;
    categoryRatios.push({ category, ratio });
  }
  
  // 비율 기준 내림차순 정렬 후 상위 9개 선택
  categoryRatios.sort((a, b) => b.ratio - a.ratio);
  const topCategories = categoryRatios.slice(0, 9);
  
  // 차트 데이터 준비
  const chartData = [{
    x: topCategories.map(item => item.category),
    y: topCategories.map(item => item.ratio),
    type: 'scatter',
    mode: 'lines+markers',
    marker: {
      color: '#4A90E2',
      size: 10
    },
    line: {
      color: '#4A90E2',
      width: 2
    },
    hovertemplate: '%{x}: %{y:.1f}%<extra></extra>'
  }];
  
  // 차트 레이아웃 설정
  const layout = {
    title: '전체 비중',
    font: {
      family: 'AppleGothic, "Malgun Gothic", sans-serif',
    },
    plot_bgcolor: '#f2f2f2',
    paper_bgcolor: '#f2f2f2',
    margin: { t: 50, b: 80, l: 50, r: 30 },
    xaxis: {
      tickangle: 0,
      title: '',
      fixedrange: true
    },
    yaxis: {
      title: '%',
      fixedrange: true
    },
    hoverlabel: {
      bgcolor: '#FFF',
      font: { size: 12, color: '#333' }
    }
  };
  
  // 차트 옵션 설정
  const config = {
    responsive: true,
    displayModeBar: false
  };
  
  // 차트 생성
  Plotly.newPlot('category-ratio-chart', chartData, layout, config);
}

/**
 * 카테고리별 전월대비 증감률 차트 생성 함수
 */
function createCategoryDeltaChart(data) {
  // 실제로는 전월 데이터도 필요하지만, 예시 데이터로 대체
  const mockDeltaData = [
    { category: '드레스', delta: 52.5 },
    { category: '캐주얼셔츠', delta: 20.8 },
    { category: '팬츠', delta: 30.9 },
    { category: '청바지', delta: 9.8 },
    { category: '니트웨어', delta: -13.6 },
    { category: '탑', delta: -17.1 },
    { category: '재킷', delta: -9.6 },
    { category: '블라우스', delta: -7.7 },
    { category: '스커트', delta: -10.5 }
  ];
  
  // 카테고리별 집계 (실제 데이터에서)
  const categoryCountMap = {};
  data.forEach(item => {
    if (item.category) {
      categoryCountMap[item.category] = (categoryCountMap[item.category] || 0) + 1;
    }
  });
  
  // 상위 카테고리 추출
  const topCategories = Object.keys(categoryCountMap)
    .map(category => ({ category, count: categoryCountMap[category] }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 9)
    .map(item => item.category);
  
  // 해당 카테고리의 증감률 데이터 필터링
  const filteredDeltaData = mockDeltaData.filter(item => 
    topCategories.includes(item.category)
  );
  
  // 차트 데이터 준비
  const chartData = [{
    x: filteredDeltaData.map(item => item.category),
    y: filteredDeltaData.map(item => item.delta),
    type: 'bar',
    marker: {
      color: filteredDeltaData.map(item => item.delta >= 0 ? '#4A90E2' : '#FF5A5A'),
    },
    hovertemplate: '%{x}: %{y:+.1f}%<extra></extra>'
  }];
  
  // 차트 레이아웃 설정
  const layout = {
    title: '전월대비 비중증가율',
    font: {
      family: 'AppleGothic, "Malgun Gothic", sans-serif',
    },
    plot_bgcolor: '#f2f2f2',
    paper_bgcolor: '#f2f2f2',
    margin: { t: 50, b: 80, l: 50, r: 30 },
    xaxis: {
      tickangle: 0,
      title: '',
      fixedrange: true
    },
    yaxis: {
      title: '%',
      fixedrange: true,
      zeroline: true,
      zerolinecolor: '#888',
      zerolinewidth: 1
    },
    hoverlabel: {
      bgcolor: '#FFF',
      font: { size: 12, color: '#333' }
    }
  };
  
  // 차트 옵션 설정
  const config = {
    responsive: true,
    displayModeBar: false
  };
  
  // 차트 생성
  Plotly.newPlot('category-delta-chart', chartData, layout, config);
}

/**
 * 브랜드별 가격대 분포 차트 생성 함수
 */
function createPriceRangeChart(data) {
  // 가격 숫자 변환 함수
  function extractPrice(priceStr) {
    if (!priceStr) return null;
    const match = priceStr.toString().replace(/[^0-9]/g, '');
    return match ? parseInt(match) : null;
  }
  
  // 브랜드별 가격 데이터 추출
  const brandPriceMap = {};
  
  data.forEach(item => {
    if (item.brand && item.price) {
      const price = extractPrice(item.price);
      if (price) {
        if (!brandPriceMap[item.brand]) {
          brandPriceMap[item.brand] = [];
        }
        brandPriceMap[item.brand].push(price);
      }
    }
  });
  
  // 브랜드별 최소, 최대, 평균 가격 계산
  const brandPriceRanges = [];
  for (const brand in brandPriceMap) {
    const prices = brandPriceMap[brand];
    if (prices.length > 0) {
      const minPrice = Math.min(...prices);
      const maxPrice = Math.max(...prices);
      const avgPrice = prices.reduce((sum, price) => sum + price, 0) / prices.length;
      
      brandPriceRanges.push({
        brand,
        minPrice,
        maxPrice,
        avgPrice,
        count: prices.length
      });
    }
  }
  
  // 평균 가격 기준 정렬하고 상위 15개 브랜드 선택
  brandPriceRanges.sort((a, b) => b.avgPrice - a.avgPrice);
  const topBrands = brandPriceRanges.slice(0, 15);
  
  // y축 설정 (상위→하위 순서로)
  const yValues = topBrands.map(item => item.brand);
  
  // 가격 범위 데이터
  const traces = [];
  
  // 가격 범위 바 트레이스
  traces.push({
    name: '가격 범위',
    y: yValues,
    x: topBrands.map(item => item.maxPrice - item.minPrice),
    base: topBrands.map(item => item.minPrice),
    type: 'bar',
    orientation: 'h',
    marker: {
      color: 'rgba(180, 180, 180, 0.7)'
    },
    hovertemplate: '가격 범위: %{base:,}원 ~ %{x:,}원<extra>%{y}</extra>'
  });
  
  // 최소 가격 스캐터 트레이스
  traces.push({
    name: '최저가격',
    y: yValues,
    x: topBrands.map(item => item.minPrice),
    type: 'scatter',
    mode: 'markers',
    marker: {
      color: '#4A90E2',
      size: 8
    },
    hovertemplate: '최저가격: %{x:,}원<extra>%{y}</extra>'
  });
  
  // 최대 가격 스캐터 트레이스
  traces.push({
    name: '최고가격',
    y: yValues,
    x: topBrands.map(item => item.maxPrice),
    type: 'scatter',
    mode: 'markers',
    marker: {
      color: '#FF5A5A',
      size: 8
    },
    hovertemplate: '최고가격: %{x:,}원<extra>%{y}</extra>'
  });
  
  // 차트 레이아웃 설정
  const layout = {
    title: '브랜드별 가격 분포',
    font: {
      family: 'AppleGothic, "Malgun Gothic", sans-serif',
    },
    plot_bgcolor: '#f2f2f2',
    paper_bgcolor: '#f2f2f2',
    margin: { t: 50, b: 50, l: 150, r: 50 },
    xaxis: {
      title: '가격 (원)',
      fixedrange: true,
      tickformat: ',d'
    },
    yaxis: {
      title: '',
      fixedrange: true,
      automargin: true
    },
    showlegend: true,
    legend: {
      orientation: 'h',
      y: -0.2
    },
    hoverlabel: {
      bgcolor: '#FFF',
      font: { size: 12, color: '#333' }
    }
  };
  
  // 차트 옵션 설정
  const config = {
    responsive: true,
    displayModeBar: false
  };
  
  // 차트 생성
  Plotly.newPlot('price-range-chart', traces, layout, config);
}

/**
 * 탭 전환 기능 초기화 - 개선된 버전
 */
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  
  if (!tabs || tabs.length === 0) {
    console.warn('탭 요소를 찾을 수 없습니다.');
    return;
  }
  
  // 이미 초기화된 탭은 재초기화하지 않음
  if (tabs[0].getAttribute('data-initialized') === 'true') {
    console.log('이미 초기화된 탭입니다.');
    return;
  }
  
  tabs.forEach(tab => {
    // 탭 초기화 표시
    tab.setAttribute('data-initialized', 'true');
    
    tab.addEventListener('click', function() {
      // 모든 탭에서 active 클래스 제거
      tabs.forEach(t => t.classList.remove('active'));
      
      // 클릭한 탭에 active 클래스 추가
      this.classList.add('active');
      
      // 모든 탭 컨텐츠 숨기기
      const tabContents = document.querySelectorAll('.tab-content');
      tabContents.forEach(content => content.classList.remove('active'));
      
      // 선택한 탭의 컨텐츠 표시
      const tabId = this.getAttribute('data-tab');
      const targetContent = document.getElementById(tabId + '-tab');
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });
  
  console.log('탭 초기화 완료');
}

/**
 * 브랜드 카드 클릭 이벤트 초기화
 */
function initBrandCards() {
  const brandItems = document.querySelectorAll('.brand-item');
  
  brandItems.forEach(item => {
    item.addEventListener('click', function() {
      // 모든 아이템에서 active 클래스 제거
      brandItems.forEach(b => b.classList.remove('active'));
      
      // 클릭한 아이템에 active 클래스 추가
      this.classList.add('active');
      
      // 브랜드 정보 가져오기
      const brandId = this.getAttribute('data-brand-id');
      const brandText = this.querySelector('.brand-text').textContent;
      // 브랜드 이름 추출 (번호 제거)
      const brandName = brandText.split('. ')[1];
      
      // 브랜드 상세 정보 API 호출
      fetchBrandDetails(brandName);
    });
  });
}

/**
 * 브랜드 상세 정보 API 호출
 * @param {string} brandName - 브랜드 이름
 */
function fetchBrandDetails(brandName) {
  // 로딩 메시지 표시
  const detailContainer = document.getElementById('brand-detail');
  if (detailContainer) {
    // 기존 차트 컨테이너와 데이터 없음 메시지 참조
    const chartContainer = document.getElementById('detail-chart-container');
    const noDataMessage = document.getElementById('detail-no-data');
    
    // 차트 컨테이너 숨기기, 로딩 표시
    if (chartContainer) chartContainer.style.display = 'none';
    if (noDataMessage) noDataMessage.style.display = 'none';
    
    // 브랜드 이름 업데이트
    const brandNameElement = detailContainer.querySelector('.detail-brand-name');
    if (brandNameElement) {
      brandNameElement.textContent = brandName;
      // 로딩 표시 추가
      brandNameElement.innerHTML = `${brandName} <small style="font-size: 0.8rem; color: #999;">(로딩 중...)</small>`;
    }
  }
  
  // API 호출
  fetch(`/api/brand-details?brand=${encodeURIComponent(brandName)}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('브랜드 정보를 불러올 수 없습니다.');
      }
      return response.json();
    })
    .then(details => {
      updateBrandDetailUI(details);
    })
    .catch(error => {
      console.error('브랜드 상세 정보 조회 오류:', error);
      displayErrorMessage(error.message);
    });
}

/**
 * 브랜드 상세 정보 UI 업데이트
 * @param {Object} details - 브랜드 상세 정보
 */
function updateBrandDetailUI(details) {
  // 상세 컨테이너 참조
  const detailContainer = document.getElementById('brand-detail');
  if (!detailContainer) return;
  
  // 기본 정보 업데이트
  const brandNameElement = detailContainer.querySelector('.detail-brand-name');
  const detailCategory = detailContainer.querySelector('.detail-category');
  const statValues = detailContainer.querySelectorAll('.stat-value');
  
  if (brandNameElement) brandNameElement.textContent = details.name;
  if (detailCategory) detailCategory.textContent = `카테고리: ${details.category}`;
  
  // 통계 값 업데이트
  if (statValues && statValues.length >= 3) {
    // 가격대 정보
    const priceRange = `${details.price_info.min_price}~${details.price_info.max_price}`;
    statValues[0].textContent = priceRange;
    
    // 성별 정보
    statValues[1].textContent = details.gender.join(', ');
    
    // 언급량 또는 평점 정보
    statValues[2].textContent = details.rating_info.avg_rating;
  }
  
  // 차트 컨테이너 업데이트
  const chartContainer = document.getElementById('detail-chart-container');
  const noDataMessage = document.getElementById('detail-no-data');
  
  if (chartContainer) {
    chartContainer.style.display = 'block';
    if (noDataMessage) noDataMessage.style.display = 'none';
    
    // 차트 데이터 생성
    chartContainer.innerHTML = `
      <div style="font-size: 0.9rem; margin-bottom: 10px; text-align: center;">
        <strong>${details.name}</strong> 월별 언급량 추이
      </div>
      <div style="display: flex; height: 100px; align-items: flex-end; justify-content: space-between; padding: 0 10px;">
        ${generateBarChart(details.monthly_data || generateDummyMonthlyData())}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #999; margin-top: 5px; padding: 0 10px;">
        ${generateMonthLabels()}
      </div>
    `;
  }
}

/**
 * 더미 월간 데이터 생성 (API가 데이터를 제공하지 않을 경우)
 * @returns {Array} 월간 데이터 배열
 */
function generateDummyMonthlyData() {
  return [
    { month: '1월', count: Math.floor(Math.random() * 1000 + 800) },
    { month: '2월', count: Math.floor(Math.random() * 1000 + 900) },
    { month: '3월', count: Math.floor(Math.random() * 1000 + 1000) },
    { month: '4월', count: Math.floor(Math.random() * 1000 + 1100) },
    { month: '5월', count: Math.floor(Math.random() * 1000 + 1200) },
    { month: '6월', count: Math.floor(Math.random() * 1000 + 1300) }
  ];
}

/**
 * 월 레이블 생성
 * @returns {string} 월 레이블 HTML
 */
function generateMonthLabels() {
  const months = ['1월', '2월', '3월', '4월', '5월', '6월'];
  return months.map(month => `<span>${month}</span>`).join('');
}

/**
 * 간단한 바 차트 생성
 * @param {Array} data - 차트 데이터
 * @returns {string} 바 차트 HTML
 */
function generateBarChart(data) {
  // 최대값 찾기
  const maxValue = Math.max(...data.map(item => item.count));
  
  // 각 월별 바 생성
  return data.map(item => {
    const height = (item.count / maxValue) * 100;
    return `
      <div style="display: flex; flex-direction: column; align-items: center; width: 30px;">
        <div style="height: ${height}%; width: 20px; background-color: #4a90e2; border-radius: 3px 3px 0 0;"></div>
      </div>
    `;
  }).join('');
}

/**
 * 오류 메시지 표시
 * @param {string} message - 오류 메시지
 */
function displayErrorMessage(message) {
  const detailContainer = document.getElementById('brand-detail');
  if (!detailContainer) return;
  
  // 브랜드 이름 요소 참조
  const brandNameElement = detailContainer.querySelector('.detail-brand-name');
  if (brandNameElement) {
    // 오류 메시지 표시
    brandNameElement.innerHTML = brandNameElement.textContent.split(' <small')[0];
  }
  
  // 카테고리 요소 참조
  const detailCategory = detailContainer.querySelector('.detail-category');
  if (detailCategory) {
    detailCategory.textContent = '카테고리: -';
  }
  
  // 통계 값 초기화
  const statValues = detailContainer.querySelectorAll('.stat-value');
  if (statValues) {
    statValues.forEach(value => {
      value.textContent = '-';
    });
  }
  
  // 차트 컨테이너 숨기기
  const chartContainer = document.getElementById('detail-chart-container');
  if (chartContainer) {
    chartContainer.style.display = 'none';
  }
  
  // 데이터 없음 메시지 표시
  const noDataMessage = document.getElementById('detail-no-data');
  if (noDataMessage) {
    noDataMessage.style.display = 'block';
    noDataMessage.textContent = `${message} 다시 시도해주세요.`;
  }
}

/**
 * 히트맵 상호작용 초기화
 */
function initHeatmapInteraction() {
  const heatmapCells = document.querySelectorAll('.grid-row:not(.header-row) .grid-cell:not(:first-child)');
  
  heatmapCells.forEach(cell => {
    cell.addEventListener('click', function() {
      // 카테고리와 미디어 타입 가져오기
      const category = this.parentElement.querySelector('.grid-cell:first-child').textContent;
      const mediaType = this.parentElement.parentElement.querySelector('.header-row .grid-cell:nth-child(' + 
                       (Array.from(this.parentElement.children).indexOf(this) + 1) + ')').textContent;
      
      // 언급량 가져오기
      const count = this.textContent;
      
      // 알림 표시 (실제 구현에서는 모달 또는 상세 정보 표시)
      alert(`${category} 카테고리의 ${mediaType} 미디어 타입 언급량: ${count}`);
    });
  });
}