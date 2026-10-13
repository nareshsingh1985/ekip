import api from "./client";

export interface SearchResult {
  score: number;
  source: string;
  text: string;
}

export const searchDocuments =
  async (query: string): Promise<SearchResult[]> => {

    const response =
      await api.post(
        "/search",
        {
          query,
        }
      );

    return response.data;
  };