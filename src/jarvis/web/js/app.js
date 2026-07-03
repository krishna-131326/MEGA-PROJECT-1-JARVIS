// app.js
// Main entry point for the frontend application

class App {
    constructor() {
        this.init();
    }

    async init() {
        // Render initial chat history
        const messages = window.stateManager.getMessages();
        const chatContainer = window.uiManager.chatContainer;
        chatContainer.innerHTML = ''; // clear default HTML message
        
        if (messages.length === 0) {
            window.uiManager.appendMessage({
                role: 'system',
                content: "Hello, I'm Jarvis. How can I help you today?"
            });
        } else {
            messages.forEach(msg => {
                window.uiManager.appendMessage(msg);
            });
        }

        // Fetch Health Data
        const healthData = await window.apiClient.checkHealth();
        window.uiManager.renderHealth(healthData);

        // Fetch Plugins
        const plugins = await window.apiClient.getPlugins();
        window.uiManager.renderPlugins(plugins);
    }
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
