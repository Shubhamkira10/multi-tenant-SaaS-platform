import api from "./axios";

export const platformLogin = async (data) => {

    const response = await api.post(
        "/auth/platform/login",
        data
    );

    return response.data.data;
};

export const tenantLogin = async (data) => {

    const response = await api.post(
        "/auth/tenant/login",
        data
    );

    return response.data;

};