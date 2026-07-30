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

export const uploadTenantData = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(
        "/tenant/upload-data",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};


export const getCurrentTenant = async () => {
    const response = await api.get("/tenant/me");
    return response.data;
};