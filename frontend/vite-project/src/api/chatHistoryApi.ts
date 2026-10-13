import api from "./client";

export const getChatHistory =
  async () => {

    const response =
      await api.get(
        "/chat/history"
      );

    return response.data;
  };