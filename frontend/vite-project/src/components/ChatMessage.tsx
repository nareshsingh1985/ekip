import {Paper, Typography, Box} from "@mui/material";
import type { Message } from "../types/chat";

interface Props {
    message: Message;
}

export default function ChatMessage({message} : Props){
    return(
        <Paper
            sx={{
                p:2,
                mb:2,
                backgroundColor:
                message.role === "user" ? "#e3f2fd" : "#f5f5f5",
            }}
        >
            <Typography>
                {message.content}
            </Typography>
            {message.sources && (
                <Box sx={{mt: 2}}>
                    <Typography variant="subtitle2">
                        Sources
                    </Typography>

                    {message.sources.map((source, index) => (
                        <Typography key={index} variant="body2">
                            {source}
                        </Typography>
                    ))}
                </Box>
            )}
        </Paper>
    );
}