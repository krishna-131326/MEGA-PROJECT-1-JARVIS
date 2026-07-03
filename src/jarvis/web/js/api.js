// api.js
// Handles communication with the FastAPI backend

class ApiClient {
    constructor() {
        this.baseUrl = window.location.origin;
    }

    async checkHealth() {
        try {
            const res = await fetch(`${this.baseUrl}/health`);
            if (!res.ok) throw new Error("Health check failed");
            return await res.json();
        } catch (e) {
            console.error("Health check error:", e);
            return null;
        }
    }

    async getPlugins() {
        try {
            const res = await fetch(`${this.baseUrl}/api/plugins`);
            if (!res.ok) throw new Error("Failed to fetch plugins");
            return await res.json();
        } catch (e) {
            console.error("Plugin fetch error:", e);
            return [];
        }
    }

    async sendMessage(message, sessionId) {
        try {
            const res = await fetch(`${this.baseUrl}/api/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId,
                    mode: "chat",
                    stream: false
                })
            });
            
            if (!res.ok) {
                throw new Error(`API Error: ${res.status}`);
            }
            return await res.json();
        } catch (e) {
            console.error("Chat API error:", e);
            throw e;
        }
    }
}

window.apiClient = new ApiClient();
