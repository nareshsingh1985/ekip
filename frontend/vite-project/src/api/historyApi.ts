import api from "./client";

export interface UploadHistoryItem {
    filename: string;
    file_type: string;
    uploaded_at?: string;
    "uploaded at"?: string;
}

export const getUploadHistory = async (): Promise<UploadHistoryItem[]> => {
    const response = await api.get("/uploads/history");
    return response.data;
};
