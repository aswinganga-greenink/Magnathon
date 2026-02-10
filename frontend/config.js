// Global configuration for API URL
let API_BASE_URL = "https://magnathon.onrender.com";

(async function determineBackend() {
    const localUrl = "http://127.0.0.1:8000";

    // If running on localhost, verify if we want to use local backend or prod
    // Logic: Try Prod. If fails, use Local.

    try {
        console.log("Checking production backend status...");
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000); // 2s timeout

        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'GET',
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (response.ok) {
            console.log("Connected to Production Backend:", API_BASE_URL);
            return;
        } else {
            throw new Error("Production backend returned non-200");
        }
    } catch (error) {
        console.warn("Production backend unreachable or timed out. Switching to Local Backend.", error);
        API_BASE_URL = localUrl;
    }
})();
