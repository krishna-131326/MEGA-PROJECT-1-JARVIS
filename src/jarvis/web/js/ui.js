// ui.js
// Handles DOM manipulation and UI states

class UIManager {
    constructor() {
        this.chatContainer = document.getElementById('chat-messages');
        this.pluginsList = document.getElementById('plugins-list');
        this.healthData = document.getElementById('health-data');
        this.healthIndicator = document.getElementById('health-indicator');
        
        this.setupNavigation();
    }

    setupNavigation() {
        const navBtns = document.querySelectorAll('.nav-btn');
        navBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                navBtns.forEach(b => b.classList.remove('active'));
                const targetBtn = e.currentTarget;
                targetBtn.classList.add('active');
                
                // Hide all views
                document.querySelectorAll('.view-panel').forEach(panel => {
                    panel.classList.remove('active');
                });
                
                // Show target view
                const viewId = `view-${targetBtn.dataset.view}`;
                document.getElementById(viewId).classList.add('active');
            });
        });
    }

    createMessageElement(message) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${message.role === 'user' ? 'user-message' : 'system-message'}`;
        
        const avatar = document.createElement('div');
        avatar.className = `avatar ${message.role === 'user' ? 'user-avatar' : 'jarvis-avatar'}`;
        avatar.textContent = message.role === 'user' ? 'U' : 'J';
        
        const contentContainer = document.createElement('div');
        contentContainer.className = 'message-content';
        
        // Render content
        if (message.role === 'user') {
            contentContainer.textContent = message.content;
        } else {
            contentContainer.innerHTML = window.markdownRenderer.render(message.content);
            if (message.pluginUsed) {
                const pluginBadge = document.createElement('div');
                pluginBadge.className = 'plugin-badge';
                pluginBadge.style.fontSize = '11px';
                pluginBadge.style.color = 'var(--text-muted)';
                pluginBadge.style.marginTop = '8px';
                pluginBadge.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" style="vertical-align: middle; margin-right: 4px;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path></svg> Via ${message.pluginUsed}`;
                contentContainer.appendChild(pluginBadge);
            }
        }

        // Action Buttons (Copy)
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions';
        const copyBtn = document.createElement('button');
        copyBtn.className = 'action-btn';
        copyBtn.textContent = 'Copy';
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(message.content);
            copyBtn.textContent = 'Copied!';
            setTimeout(() => copyBtn.textContent = 'Copy', 2000);
        };
        actionsDiv.appendChild(copyBtn);
        contentContainer.appendChild(actionsDiv);

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(contentContainer);
        return msgDiv;
    }

    appendMessage(message) {
        const el = this.createMessageElement(message);
        this.chatContainer.appendChild(el);
        this.scrollToBottom();
    }

    showThinkingState(stateText = "Jarvis is reasoning...") {
        this.removeThinkingState();
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system-message thinking-message';
        msgDiv.id = 'thinking-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar jarvis-avatar';
        avatar.textContent = 'J';
        
        const contentContainer = document.createElement('div');
        contentContainer.className = 'message-content';
        contentContainer.style.display = 'flex';
        contentContainer.style.alignItems = 'center';
        contentContainer.style.gap = '8px';
        contentContainer.style.color = 'var(--text-muted)';
        
        const text = document.createElement('span');
        text.textContent = stateText;
        
        const dots = document.createElement('div');
        dots.className = 'thinking-dots';
        dots.innerHTML = '<span></span><span></span><span></span>';
        
        contentContainer.appendChild(text);
        contentContainer.appendChild(dots);
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(contentContainer);
        
        this.chatContainer.appendChild(msgDiv);
        this.scrollToBottom();
    }

    removeThinkingState() {
        const existing = document.getElementById('thinking-indicator');
        if (existing) {
            existing.remove();
        }
    }

    scrollToBottom() {
        this.chatContainer.scrollTo({
            top: this.chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    renderHealth(data) {
        if (!data) {
            this.healthData.textContent = "Unable to fetch health data.";
            this.healthIndicator.className = "status-dot";
            return;
        }
        this.healthData.textContent = JSON.stringify(data, null, 4);
        if (data.status === 'healthy') {
            this.healthIndicator.className = "status-dot healthy";
        }
    }

    renderPlugins(plugins) {
        this.pluginsList.innerHTML = '';
        if (!plugins || plugins.length === 0) {
            this.pluginsList.innerHTML = '<li>No plugins active.</li>';
            return;
        }
        
        plugins.forEach(p => {
            const li = document.createElement('li');
            li.className = 'plugin-card';
            li.innerHTML = `
                <svg class="plugin-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>${p.name}</span>
            `;
            this.pluginsList.appendChild(li);
        });
    }
}

window.uiManager = new UIManager();
