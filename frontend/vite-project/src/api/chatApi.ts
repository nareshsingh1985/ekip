import api from "./client";

export interface ChatResponse {
  answer: string;
  sources: string[];
}

export const askQuestion = async (
  question: string,
): Promise<ChatResponse> => {
  const response = await api.post("/chat", { question });
  return response.data;
};
