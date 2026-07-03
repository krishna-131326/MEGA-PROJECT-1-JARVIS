// chat.js
// Handles chat interaction logic

class ChatController {
    constructor() {
        this.input = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.clearBtn = document.getElementById('clear-chat-btn');
        this.isProcessing = false;

        this.setupEventListeners();
    }

    setupEventListeners() {
        // Send on click
        this.sendBtn.addEventListener('click', () => this.handleSend());

        // Keyboard UX
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // Global Keyboard UX
        document.addEventListener('keydown', (e) => {
            // Ctrl+L to clear chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                this.clearChat();
            }
            
            // Focus input on any keypress if not already focused and not typing in another input
            if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && document.activeElement !== this.input) {
                this.input.focus();
            }
        });

        this.clearBtn.addEventListener('click', () => this.clearChat());

        // Auto-resize textarea
        this.input.addEventListener('input', () => {
            this.input.style.height = 'auto';
            this.input.style.height = Math.min(this.input.scrollHeight, 200) + 'px';
            this.sendBtn.disabled = this.input.value.trim().length === 0;
        });
    }

    async handleSend() {
        const text = this.input.value.trim();
        if (!text || this.isProcessing) return;

        // Reset input
        this.input.value = '';
        this.input.style.height = 'auto';
        this.sendBtn.disabled = true;
        this.isProcessing = true;

        // Add User Message
        const userMsg = window.stateManager.addMessage('user', text);
        window.uiManager.appendMessage(userMsg);

        // Show thinking
        window.uiManager.showThinkingState("Jarvis is reasoning...");

        try {
            const sessionId = window.stateManager.getSessionId();
            const response = await window.apiClient.sendMessage(text, sessionId);
            
            window.uiManager.removeThinkingState();
            
            // Add System Message
            const sysMsg = window.stateManager.addMessage(
                'system', 
                response.response, 
                response.plugin_used
            );
            window.uiManager.appendMessage(sysMsg);
            
        } catch (e) {
            window.uiManager.removeThinkingState();
            const errMsg = window.stateManager.addMessage('system', 'Error connecting to the Jarvis backend.');
            window.uiManager.appendMessage(errMsg);
        } finally {
            this.isProcessing = false;
            this.input.focus();
        }
    }

    clearChat() {
        window.stateManager.clearMessages();
        window.uiManager.chatContainer.innerHTML = '';
        // Add greeting
        const greeting = {
            role: 'system',
            content: "Hello, I'm Jarvis. How can I help you today?"
        };
        window.uiManager.appendMessage(greeting);
    }
}

window.chatController = new ChatController();
