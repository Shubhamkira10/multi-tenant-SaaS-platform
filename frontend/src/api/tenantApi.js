import api from "./axios";

export const getTenants = async () => {
    const response = await api.get("/tenants");
    return response.data;
};

export const createTenant = async (data) => {
    const response = await api.post("/tenants", data);
    return response.data;
};

export const updateTenant = async (uuid, data) => {
    const response = await api.put(`/tenants/${uuid}`, data);
    return response.data;
};

export const deleteTenant = async (uuid) => {
    const response = await api.delete(`/tenants/${uuid}`);
    return response.data;
};