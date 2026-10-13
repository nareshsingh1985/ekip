import api from "./client";

export interface InsightResponse {
    result: string;
}

export const getSummary = async (): Promise<InsightResponse> => {
    const response = await api.get("/insights/summary");
    return response.data;
};

export const getRisks = async (): Promise<InsightResponse> => {
    const response = await api.get("/insights/risks");
    return response.data;
};

export const getActions = async (): Promise<InsightResponse> => {
    const response = await api.get("/insights/actions");
    return response.data;
};