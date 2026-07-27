import api from "./axios";

export const getUsers = async () => {
    const response = await api.get("/users");
    return response.data;
};

export const createAgent = async (data) => {
    const response = await api.post("/users/agents", data);
    return response.data;
};

export const updateUser = async (uuid, data) => {
    const response = await api.put(`/users/${uuid}`, data);
    return response.data;
};

export const deleteUser = async (uuid) => {
    const response = await api.delete(`/users/${uuid}`);
    return response.data;
};