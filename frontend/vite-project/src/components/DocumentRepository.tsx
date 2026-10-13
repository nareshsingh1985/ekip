import {
  Alert,
  CircularProgress,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

import {
  useEffect,
  useState,
} from "react";

import {
  getDocuments
} from "../api/documentApi";
import type { UploadHistoryItem } from "../api/historyApi";

export default function DocumentRepository() {

  const [documents, setDocuments] =
    useState<UploadHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadDocuments = async () => {
      try {
        const data = await getDocuments();
        if (isMounted) {
          setDocuments(data);
        }
      } catch {
        if (isMounted) {
          setError("Unable to load the document repository.");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    void loadDocuments();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <Paper sx={{ p: 3, mb: 3 }}>

      <Typography
        variant="h6"
        gutterBottom
      >
        Document Repository
      </Typography>

      {loading && <CircularProgress aria-label="Loading document repository" />}
      {error && <Alert severity="error">{error}</Alert>}
      {!loading && !error && documents.length === 0 && (
        <Typography color="text.secondary">No documents uploaded yet.</Typography>
      )}
      {!loading && !error && documents.length > 0 && <Table>

        <TableHead>
          <TableRow>

            <TableCell>
              Document Name
            </TableCell>

            <TableCell>
              Type
            </TableCell>

            <TableCell>
              Upload Date
            </TableCell>

          </TableRow>
        </TableHead>

        <TableBody>

          {documents.map(
            (doc, index) => (
              <TableRow key={`${doc.filename}-${doc.uploaded_at ?? doc["uploaded at"] ?? index}`}>

                <TableCell>
                  {doc.filename}
                </TableCell>

                <TableCell>
                  {doc.file_type}
                </TableCell>

                <TableCell>
                  {doc.uploaded_at ?? doc["uploaded at"] ?? "—"}
                </TableCell>

              </TableRow>
            )
          )}

        </TableBody>

      </Table>}

    </Paper>
  );
}
