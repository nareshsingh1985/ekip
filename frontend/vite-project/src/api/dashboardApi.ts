import api from "./client";

export interface DashboardStats {
    documents: number;
    vectors: number;
    collection: string;
    status: string;
}

export const getDashboardStats = async (): Promise<DashboardStats> => {
    const response = await api.get("/dashboard/stats");
    return response.data;
};