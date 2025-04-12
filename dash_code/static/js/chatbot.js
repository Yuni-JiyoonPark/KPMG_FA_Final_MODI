/**
 * chatbot.js - 대시보드 사이드바 챗봇 기능 구현
 * 질의응답 시스템을 대시보드에 통합된 사이드바 형태로 제공
 */

document.addEventListener('DOMContentLoaded', function() {
  initChatbot();
});

/**
* 챗봇 기능 초기화
*/
function initChatbot() {
  // DOM 요소 참조
  const chatbotToggle = document.getElementById('chatbot-toggle');
  const chatbotSidebar = document.getElementById('chatbot-sidebar');
  const chatbotClose = document.getElementById('chatbot-close');
  const chatbotInput = document.getElementById('chatbot-input');
  const chatbotSend = document.getElementById('chatbot-send');
  const chatbotConversation = document.getElementById('chatbot-conversation');
  const exampleQueries = document.querySelectorAll('.chatbot-example-query');
  
  // 요소가 존재하는지 확인
  if (!chatbotToggle || !chatbotSidebar || !chatbotClose || !chatbotInput || !chatbotSend || !chatbotConversation) {
    console.error('일부 챗봇 요소를 찾을 수 없습니다.');
    return;
  }
  
  // 챗봇 사이드바 토글
  chatbotToggle.addEventListener('click', function() {
    chatbotSidebar.classList.add('active');
    chatbotInput.focus(); // 입력란에 포커스
  });
  
  chatbotClose.addEventListener('click', function() {
    chatbotSidebar.classList.remove('active');
  });
  
  // ESC 키를 누르면 닫기
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && chatbotSidebar.classList.contains('active')) {
      chatbotSidebar.classList.remove('active');
    }
  });
  
  // 외부 클릭시 닫기 (선택적)
  document.addEventListener('click', function(e) {
    if (chatbotSidebar.classList.contains('active') && 
        !chatbotSidebar.contains(e.target) && 
        e.target !== chatbotToggle &&
        !chatbotToggle.contains(e.target)) {
      chatbotSidebar.classList.remove('active');
    }
  });
  
  // 메시지 전송 함수
  function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;
    
    // 사용자 메시지 추가
    addMessage('user', message);
    chatbotInput.value = '';
    
    // 로딩 표시 추가
    const loadingElement = document.createElement('div');
    loadingElement.className = 'chatbot-loading';
    loadingElement.innerHTML = `
      <div class="chatbot-loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;
    chatbotConversation.appendChild(loadingElement);
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    
    // 특수 메시지 처리: 리포트 요청
    if (message.toLowerCase().includes('레포트를 작성해줘') || message.toLowerCase().includes('리포트를 작성해줘')) {
      // 로딩 제거
      setTimeout(() => {
        if (loadingElement.parentNode) {
          chatbotConversation.removeChild(loadingElement);
        }
        
        // 리포트 응답 추가
        addMessage('assistant', '레포트가 작성되었습니다. <a href="#" class="show-report-link">레포트 보기</a>');
        
        // 레포트 링크에 이벤트 리스너 추가
        const reportLinks = document.querySelectorAll('.show-report-link');
        reportLinks.forEach(link => {
          link.addEventListener('click', function(e) {
            e.preventDefault();
            showReport();
          });
        });
      }, 1500); // 실제 API 호출처럼 보이기 위한 지연
      
      return; // 기존 API 호출 방지
    }
    
    // 데이터 소스 및 날짜 범위 가져오기
    const dataSource = document.querySelector('input[name="chatbot-data-source"]:checked').value;
    const startDate = document.getElementById('chatbot-start-date').value;
    const endDate = document.getElementById('chatbot-end-date').value;
    
    // API 호출
    fetch('/api/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message,
        data_source: dataSource,
        start_date: startDate,
        end_date: endDate
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`API 호출 오류: ${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      // 로딩 제거
      if (loadingElement.parentNode) {
        chatbotConversation.removeChild(loadingElement);
      }
      
      // 응답 추가
      if (data.error) {
        addMessage('assistant', '죄송합니다. 오류가 발생했습니다: ' + data.error);
      } else {
        addMessage('assistant', data.response || '응답이 없습니다.');
      }
    })
    .catch(error => {
      // 로딩 제거
      if (loadingElement.parentNode) {
        chatbotConversation.removeChild(loadingElement);
      }
      
      console.error('Error:', error);
      addMessage('assistant', '죄송합니다. 요청을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.');
    });
  }
  
  // 메시지 추가 함수
  function addMessage(type, content) {
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${type}`;
    
    // 마크다운 변환 (외부 라이브러리 필요)
    if (type === 'assistant' && window.marked) {
      messageElement.innerHTML = marked.parse(content);
    } else {
      messageElement.textContent = content;
    }
    
    chatbotConversation.appendChild(messageElement);
    scrollToBottom();
  }
  
  // 채팅창 스크롤 맨 아래로 내리기
  function scrollToBottom() {
    setTimeout(() => {
      chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    }, 50); // 약간의 지연을 줘서 내용이 완전히 렌더링 후에 스크롤
  }
  
  // 이벤트 리스너 등록
  chatbotSend.addEventListener('click', sendMessage);
  
  chatbotInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault(); // 폼 제출 방지
      sendMessage();
    }
  });
  
  // 예시 질문 클릭 이벤트
  exampleQueries.forEach(query => {
    query.addEventListener('click', function() {
      chatbotInput.value = this.textContent;
      sendMessage();
    });
  });
  
  // 현재 날짜 기준으로 기본 날짜 범위 설정
  setupDefaultDates();
}

/**
* 현재 날짜 기준으로 기본 날짜 범위 설정
*/
function setupDefaultDates() {
try {
  const today = new Date();
  const endDateInput = document.getElementById('chatbot-end-date');
  const startDateInput = document.getElementById('chatbot-start-date');
  
  if (endDateInput) {
    endDateInput.value = formatDate(today);
  }
  
  if (startDateInput) {
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(today.getDate() - 7);
    startDateInput.value = formatDate(sevenDaysAgo);
  }
} catch (e) {
  console.error('날짜 초기화 오류:', e);
}
}

/**
* 날짜를 YYYY-MM-DD 형식으로 변환
*/
function formatDate(date) {
const year = date.getFullYear();
const month = String(date.getMonth() + 1).padStart(2, '0');
const day = String(date.getDate()).padStart(2, '0');
return `${year}-${month}-${day}`;
}

/**
* 시스템 메시지 추가
* - 미리 준비된 도움말 메시지나 환영 메시지 등을 화면에 추가
*/
function addSystemMessages() {
const chatbotConversation = document.getElementById('chatbot-conversation');
if (!chatbotConversation) return;

// 기존 시스템 메시지 확인 (중복 방지)
const existingSystemMessages = chatbotConversation.querySelectorAll('.chat-message.system');
if (existingSystemMessages.length > 0) return;

// 환영 메시지 추가
const welcomeMessage = document.createElement('div');
welcomeMessage.className = 'chat-message system';
welcomeMessage.innerHTML = `
  <p>안녕하세요! 패션 트렌드에 관한 질문이 있으신가요?</p>
  <p>데이터 소스와 날짜 범위를 선택하고 질문을 입력해주세요. 📊</p>
`;

chatbotConversation.appendChild(welcomeMessage);
}

// 추가 기능: 웹 소켓 연결이 필요한 경우
function setupWebSocket() {
// 필요한 경우 웹소켓 연결 코드 작성
}

// 추가 기능: 채팅 내역 저장
function saveChatHistory() {
// sessionStorage나 localStorage에 대화 내용 저장 기능 구현
}

// 추가 기능: 채팅 내역 불러오기
function loadChatHistory() {
// 저장된 대화 내용 불러오기 기능 구현
}

// 필요한 경우 웹소켓 이벤트 처리
window.addEventListener('beforeunload', function() {
// 웹소켓 연결 종료나 자원 정리 코드
});

/**
* 리포트 오버레이 표시 함수
*/
function showReport() {
const reportOverlay = document.getElementById('report-overlay');
const reportContent = document.getElementById('report-content');
const reportCloseBtn = document.getElementById('report-close-btn');
const reportCopyBtn = document.getElementById('report-copy-btn');
const reportSaveBtn = document.getElementById('report-save-btn');

if (!reportOverlay || !reportContent) {
  console.error('리포트 요소를 찾을 수 없습니다.');
  return;
}

// 하드코딩된 리포트 내용
const reportHTML = `
  <h2>Z세대 중심 커머스 플랫폼 트렌드 인사이트 리포트</h2>
  
  <h3>1. 트렌드 키워드 및 설명</h3>
  <ul>
    <li><strong>Layered Luxe:</strong> 레이어드 스타일의 고급스러움이 부각되며, 다양한 아이템을 겹쳐 입는 방식이 인기를 끌고 있습니다.</li>
    <li><strong>Chic Accessories:</strong> 세련된 액세서리에 대한 수요가 증가하며, 고급 소재와 독특한 디자인의 주얼리가 주목받고 있습니다.</li>
    <li><strong>Sporty Elegance:</strong> 스포티함과 우아함을 결합한 스타일이 부상하고 있으며, 미니멀리즘 트렌드가 인기를 얻고 있습니다.</li>
  </ul>
  
  <h3>2. 연관 아이템 분석</h3>
  <ul>
    <li><strong>Layered Luxe:</strong>
      <ul>
        <li>브랜드: The Row, Balenciaga</li>
        <li>상품: 레이어드 재킷, 스퀘어토 부츠</li>
        <li>가격대: 100,000원 ~ 500,000원</li>
      </ul>
    </li>
    <li><strong>Chic Accessories:</strong>
      <ul>
        <li>브랜드: Dior, Fred</li>
        <li>상품: 핑크 골드 링, 다이아몬드 이어링</li>
        <li>가격대: 200,000원 ~ 1,000,000원</li>
      </ul>
    </li>
    <li><strong>Sporty Elegance:</strong>
      <ul>
        <li>브랜드: Nike, Adidas</li>
        <li>상품: 스포티한 원피스, 캐주얼 셔츠</li>
        <li>가격대: 50,000원 ~ 300,000원</li>
      </ul>
    </li>
  </ul>
  
  <h3>3. 부상 배경 분석</h3>
  <ul>
    <li><strong>사회/문화/경제 변화:</strong> 팬데믹 이후 개인화된 스타일과 집에서의 활동 증가로 인해 편안하면서도 스타일리시한 의류 수요가 확대되었습니다.</li>
    <li><strong>소비자 심리/니즈:</strong> Z세대는 독창성을 중시하며, 개성을 표현할 수 있는 아이템을 선호하는 경향이 있습니다.</li>
    <li><strong>확산 출처:</strong> 인플루언서와 패션 블로거들이 SNS 플랫폼을 통해 이 트렌드를 적극적으로 홍보하고 있습니다.</li>
  </ul>
  
  <h3>4. 매거진별 트렌드 요약</h3>
  <ul>
    <li><strong>Layered Luxe:</strong> 매거진에서는 레이어드 스타일을 통해 개성을 강조하고, 다양한 조합의 가능성을 소개하고 있습니다.</li>
  </ul>
`;

// 이벤트 리스너 제거 (중복 방지)
if (reportCloseBtn) {
  reportCloseBtn.removeEventListener('click', closeReport);
  reportCloseBtn.addEventListener('click', closeReport);
}

if (reportCopyBtn) {
  reportCopyBtn.removeEventListener('click', copyReportToClipboard);
  reportCopyBtn.addEventListener('click', copyReportToClipboard);
}

if (reportSaveBtn) {
  reportSaveBtn.removeEventListener('click', saveReportAsPDF);
  reportSaveBtn.addEventListener('click', saveReportAsPDF);
}

// 오버레이 클릭 이벤트 (중복 방지)
reportOverlay.removeEventListener('click', handleOverlayClick);
reportOverlay.addEventListener('click', handleOverlayClick);

// ESC 키 이벤트 제거 (중복 방지)
document.removeEventListener('keydown', handleEscKeyForReport);
document.addEventListener('keydown', handleEscKeyForReport);

// 리포트 내용 설정
reportContent.innerHTML = reportHTML;

// 오버레이 표시
reportOverlay.classList.add('active');
}

// 리포트 오버레이 닫기 함수
function closeReport() {
const reportOverlay = document.getElementById('report-overlay');
if (reportOverlay) {
  reportOverlay.classList.remove('active');
}
}

// 오버레이 영역 클릭 시 닫기
function handleOverlayClick(e) {
if (e.target === this) {
  closeReport();
}
}

// ESC 키로 리포트 닫기
function handleEscKeyForReport(e) {
const reportOverlay = document.getElementById('report-overlay');
if (e.key === 'Escape' && reportOverlay && reportOverlay.classList.contains('active')) {
  closeReport();
}
}

/**
* 리포트 내용을 클립보드에 복사
*/
function copyReportToClipboard() {
const reportContent = document.getElementById('report-content');

if (!reportContent) {
  console.error('리포트 내용을 찾을 수 없습니다.');
  return;
}

const text = reportContent.innerText;

// 클립보드에 복사
navigator.clipboard.writeText(text)
  .then(() => {
    alert('리포트가 클립보드에 복사되었습니다.');
  })
  .catch(err => {
    console.error('클립보드 복사 실패:', err);
    alert('클립보드 복사에 실패했습니다.');
  });
}

/**
* 리포트를 PDF로 저장 (간단한 구현)
*/
function saveReportAsPDF() {
alert('PDF 저장 기능은 실제 서비스에서 구현될 예정입니다.');
// 실제 구현에서는 html2pdf.js 등의 라이브러리를 사용하여 PDF 변환 구현
}