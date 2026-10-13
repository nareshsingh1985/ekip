import {
    Alert,
    CircularProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { getUploadHistory } from "../api/historyApi";
import type { UploadHistoryItem } from "../api/historyApi";

export default function UploadHistory() {
    const [uploads, setUploads] = useState<UploadHistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        const loadHistory = async () => {
            try {
                const data = await getUploadHistory();
                if (isMounted) {
                    setUploads(data);
                }
            } catch {
                if (isMounted) {
                    setError("Unable to load upload history.");
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        void loadHistory();
        return () => {
            isMounted = false;
        };
    }, []);

    return (
        <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" component="h2" gutterBottom>
                Recent Uploads
            </Typography>
            {loading && <CircularProgress aria-label="Loading upload history" />}
            {error && <Alert severity="error">{error}</Alert>}
            {!loading && !error && uploads.length === 0 && (
                <Typography color="text.secondary">No documents uploaded yet.</Typography>
            )}
            {!loading && !error && uploads.length > 0 && <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>File Name</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Uploaded at</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {uploads.map((item, index) => (
                        <TableRow key={`${item.filename}-${item.uploaded_at ?? item["uploaded at"] ?? index}`}>
                            <TableCell>{item.filename}</TableCell>
                            <TableCell>{item.file_type}</TableCell>
                            <TableCell>{item.uploaded_at ?? item["uploaded at"] ?? "—"}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>}
        </Paper>
    );
}