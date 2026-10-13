import api from "./client";

export interface UploadResponse {
    status: string;
    filename: string;
}

export const uploadFile = async (
    file: File
): Promise<UploadResponse> => {
    const formData = new FormData();

    formData.append("file", file);
    const response = await api.post("/upload", formData);
    return response.data;
};