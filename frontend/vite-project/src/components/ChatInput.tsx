import { Button, Stack, TextField } from "@mui/material";
import { useState } from "react";

interface Props{
    onSend: (message: string) => Promise<void>;
    disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: Props) {
    const [question, setQuestion] = useState("");
    const handleSend = async () => {
        const trimmedQuestion = question.trim();
        if (!trimmedQuestion || disabled) {
            return;
        }
        await onSend(trimmedQuestion);
        setQuestion("");
    };

    return (
        <Stack direction="row" spacing={2}>
            <TextField
                fullWidth
                label="Ask a Question"
                value={question}
                disabled={disabled}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={async (event) => {
                    if (event.key === "Enter" && !event.shiftKey) {
                        event.preventDefault();
                        await handleSend();
                    }
                }}
            />
            <Button
                variant="contained"
                disabled={disabled || !question.trim()}
                onClick={handleSend}
            >
                {disabled ? "Thinking…" : "Send"}
            </Button>
        </Stack>
    );
}
