import api from "./client";

export interface UploadResponse {
    status: string;
    filename: string;
}

export const SUPPORTED_UPLOAD_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".xls",
    ".xlsx",
    ".json",
];

export const uploadFile = async (
    file: File
): Promise<UploadResponse> => {
    const formData = new FormData();

    formData.append("file", file);
    const response = await api.post<UploadResponse>("/upload", formData);
    return response.data;
};