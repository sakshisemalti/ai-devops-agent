// frontend/src/services/api.js
import axios from "axios";

// Use environment variable if available, otherwise fallback to localhost
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Example API calls
export const triggerFixAndPR = async (repoName) => {
  const response = await api.post("/fix-and-pr", { repo: repoName });
  return response.data;
};

export const getPRStatus = async () => {
  const response = await api.get("/pr-status");
  return response.data;
};

export const connectRepo = async (repoName) => {
  const response = await api.post("/connect-repo", { repo: repoName });
  return response.data;
};

export default api;
