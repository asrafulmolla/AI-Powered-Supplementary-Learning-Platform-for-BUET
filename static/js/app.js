document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    if (chatInput && sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    async function sendMessage() {
        const query = chatInput.value.trim();
        if (!query) return;

        // Add user message
        appendMessage(query, 'user');
        chatInput.value = '';

        // Show loading state
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message ai';
        loadingDiv.textContent = 'Thinking...';
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const banglaMode = document.getElementById('bangla-mode')?.checked || false;
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    query: query,
                    bangla_mode: banglaMode
                })
            });

            const data = await response.json();

            chatMessages.removeChild(loadingDiv);

            if (data.answer) {
                let answerHTML = `<div>${data.answer}</div>`;
                if (data.sources && data.sources.length > 0) {
                    answerHTML += `<div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #cbd5e1; font-size: 0.75rem; color: var(--text-muted);">
                        <b>Sources:</b> ${data.sources.map(s => `<a href="/material-detail/${s.id}/" style="color: var(--primary); text-decoration: none;">${s.title}</a>`).join(', ')}
                    </div>`;
                }
                appendHTMLMessage(answerHTML, 'ai');
            } else {
                appendMessage("Sorry, I encountered an error.", 'ai');
            }

        } catch (error) {
            chatMessages.removeChild(loadingDiv);
            console.error('Error:', error);
            appendMessage("Network error. Please try again.", 'ai');
        }
    }

    function appendMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.innerText = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendHTMLMessage(html, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.innerHTML = html;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
