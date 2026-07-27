import api from "./axios";

export const getFeatures = async () => {
    const response = await api.get("/features");
    return response.data;
};

export const createFeature = async (data) => {
    const response = await api.post("/features", data);
    return response.data;
};

export const updateFeature = async (uuid, data) => {
    const response = await api.put(`/features/${uuid}`, data);
    return response.data;
};

export const deleteFeature = async (uuid) => {
    const response = await api.delete(`/features/${uuid}`);
    return response.data;
};