import api from "./axios";

export const assignFeatureToTenant = async (data) => {
    const response = await api.post(
        "/rbac/tenants/features",
        data
    );

    return response.data;
};

export const getTenantFeatures = async (tenantUuid) => {
    const response = await api.get(
        `/rbac/tenants/${tenantUuid}/features`
    );

    return response.data;
};

export const removeFeatureFromTenant = async (
    tenantUuid,
    featureUuid
) => {
    const response = await api.delete(
        `/rbac/tenants/${tenantUuid}/features/${featureUuid}`
    );

    return response.data;
};