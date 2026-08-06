import api from "./axios";

export const fetchPlatformDashboard = async () => {
    const response = await api.get("/dashboard");
    return response.data.data;
};