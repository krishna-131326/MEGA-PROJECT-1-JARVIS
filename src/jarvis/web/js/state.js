// state.js
// Manages global application state and persistence

class StateManager {
    constructor() {
        this.STORAGE_KEY = 'jarvis_chat_state';
        this.state = this.loadState() || this.getInitialState();
    }

    getInitialState() {
        return {
            sessionId: typeof uuid !== 'undefined' ? uuid.v4() : crypto.randomUUID(),
            messages: []
        };
    }

    loadState() {
        try {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            return saved ? JSON.parse(saved) : null;
        } catch (e) {
            console.error("Failed to load state from localStorage:", e);
            return null;
        }
    }

    saveState() {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.state));
        } catch (e) {
            console.error("Failed to save state to localStorage:", e);
        }
    }

    addMessage(role, content, pluginUsed = null) {
        const message = {
            id: typeof uuid !== 'undefined' ? uuid.v4() : crypto.randomUUID(),
            role,
            content,
            pluginUsed,
            timestamp: new Date().toISOString()
        };
        this.state.messages.push(message);
        this.saveState();
        return message;
    }

    clearMessages() {
        this.state.messages = [];
        this.saveState();
    }

    getMessages() {
        return this.state.messages;
    }

    getSessionId() {
        return this.state.sessionId;
    }
}

window.stateManager = new StateManager();
