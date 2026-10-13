import api from "./client";
import type { UploadHistoryItem } from "./historyApi";

export const getDocuments =
  async (): Promise<UploadHistoryItem[]> => {

    const response =
      await api.get(
        "/documents"
      );

    return response.data;
  };