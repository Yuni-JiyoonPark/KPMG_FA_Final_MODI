// 탭 전환 기능
function showTab(tabId) {
    // 모든 탭 내용 숨기기
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // 모든 탭 버튼 비활성화
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // 선택한 탭 내용과 버튼 활성화
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// 질문 보내기
async function sendQuery() {
    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();
    
    if (!query) return;
    
    // 사용자 메시지 표시
    addMessage('user', query);
    
    // 입력창 비우기
    queryInput.value = '';
    
    // 로딩 표시
    const loadingId = addMessage('bot', '<div class="loading">처리 중</div>');
    
    try {
        // API 요청
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        });
        
        if (!response.ok) {
            throw new Error('API 요청 실패');
        }
        
        const data = await response.json();
        
        // 로딩 메시지 제거
        removeMessage(loadingId);
        
        // 응답 표시
        addMessage('bot', data.response);
    } catch (error) {
        console.error('Error:', error);
        
        // 로딩 메시지 제거
        removeMessage(loadingId);
        
        // 에러 메시지 표시
        addMessage('bot', '요청 처리 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
}

// 메시지 추가
function addMessage(type, content) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    
    messageElement.classList.add('message');
    messageElement.classList.add(type === 'user' ? 'user-message' : 'bot-message');
    
    const messageId = 'msg-' + Date.now();
    messageElement.id = messageId;
    
    if (type === 'bot' && !content.includes('<div class="loading">')) {
        // 마크다운 변환 (봇 메시지만)
        messageElement.innerHTML = marked.parse(content);
    } else {
        messageElement.innerHTML = content;
    }
    
    messagesContainer.appendChild(messageElement);
    
    // 스크롤을 최하단으로
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageId;
}

// 메시지 제거
function removeMessage(messageId) {
    const messageElement = document.getElementById(messageId);
    if (messageElement) {
        messageElement.remove();
    }
}

// 레포트 생성
async function generateReport() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (!startDate || !endDate) {
        alert('시작일과 종료일을 모두 선택해주세요.');
        return;
    }
    
    const reportContent = document.getElementById('report-content');
    reportContent.innerHTML = '<div class="loading">레포트 생성 중</div>';
    
    try {
        // API 요청
        const response = await fetch('/api/generate-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_date: startDate + ' 00:00:00',
                end_date: endDate + ' 23:59:59'
            }),
        });
        
        if (!response.ok) {
            throw new Error('API 요청 실패');
        }
        
        const data = await response.json();
        
        // 마크다운 변환하여 표시
        reportContent.innerHTML = marked.parse(data.report);
    } catch (error) {
        console.error('Error:', error);
        reportContent.innerHTML = '<p class="error">레포트 생성 중 오류가 발생했습니다. 다시 시도해주세요.</p>';
    }
}

// 엔터 키로 질문 전송
document.getElementById('query-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendQuery();
    }
});