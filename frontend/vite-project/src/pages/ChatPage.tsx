import {
  Box,
  Container,
  Typography,
  CircularProgress,
} from "@mui/material";

import { useState } from "react";

import Dashboard from "../components/Dashboard";
import EnterpriseSearch from "../components/EnterpriseSearch";
import FileUploader from "../components/FileUploader";
import UploadHistory from "../components/UploadHistory";
import DocumentRepository from "../components/DocumentRepository";
import InsightsPanel from "../components/InsightsPanel";
import KnowledgeGraph from "../components/KnowledgeGraph";

import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";

import { askQuestion } from "../api/chatApi";
import type { Message } from "../types/chat";

export default function ChatPage() {

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [loading, setLoading] =
    useState(false);

  const handleSend = async (
    question: string
  ) => {

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    try {

      setLoading(true);

      const response =
        await askQuestion(question);

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Error communicating with backend.",
        },
      ]);

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  return (

    <Container maxWidth="lg">

      <Typography
        variant="h4"
        sx={{ mt: 4 }}
      >
        EKIP
      </Typography>

      <Typography
        variant="h6"
        color="text.secondary"
        sx={{ mb: 2 }}
      >
        Enterprise Knowledge Intelligence Platform
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        AI-Powered Enterprise Search,
        Knowledge Discovery,
        Executive Insights,
        and Document Intelligence
      </Typography>

      <Dashboard />

      <EnterpriseSearch />

      <FileUploader />

      <UploadHistory />

      <DocumentRepository />

      <InsightsPanel />

      <KnowledgeGraph />

      <Typography
        variant="h5"
        sx={{ mb: 2 }}
      >
        AI Assistant
      </Typography>

      <Box sx={{ mb: 4 }}>

        {messages.map(
          (message, index) => (
            <ChatMessage
              key={index}
              message={message}
            />
          )
        )}

        {loading && (
          <CircularProgress />
        )}

      </Box>

      <ChatInput
        onSend={handleSend}
      />

    </Container>
  );
}