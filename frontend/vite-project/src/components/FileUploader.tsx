import {useState} from 'react';

import { Alert, Button, Paper, Typography } from "@mui/material";

import { uploadFile } from "../api/uploadApi";

export default function FileUploader() {
    const [message, setMessage] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [uploading, setUploading] = useState(false);

    const handleUpload = async (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const file = event.target.files?.[0];

        if (!file) {
            return;
        }

        setError(null);
        setMessage("");
        setUploading(true);
        try {
            const result = await uploadFile(file);
            setMessage(`Uploaded successfully: ${result.filename}`);
        } catch {
            setError("File upload failed. Please try again.");
        } finally {
            setUploading(false);
            event.target.value = "";
        }
    };
    return (
        <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" component="h2" gutterBottom>
                Upload Documents
            </Typography>
            <Button variant="contained" component="label" disabled={uploading}>
                {uploading ? "Uploading…" : "Select File"}
                <input
                    hidden
                    type="file"
                    onChange={handleUpload}
                    aria-label="Select a document to upload"
                />
            </Button>
            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
            {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
        </Paper>
    );
}