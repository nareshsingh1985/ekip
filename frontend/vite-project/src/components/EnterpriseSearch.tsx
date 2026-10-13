import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
} from "@mui/material";

import { useState } from "react";

import {
  searchDocuments
} from "../api/searchApi";
import type { SearchResult } from "../api/searchApi";

export default function EnterpriseSearch() {

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runSearch =
    async () => {

      if (!query.trim()) {
        return;
      }

      setLoading(true);
      setError(null);
      try {

        const data =
          await searchDocuments(
            query.trim()
          );

        setResults(data);

      } catch {
        setError("Unable to search documents. Please try again.");
      } finally {
        setLoading(false);
      }
    };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>

      <Typography
        variant="h6"
        gutterBottom
      >
        Enterprise Search
      </Typography>

      <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
        <TextField
          fullWidth
          label="Search enterprise knowledge"
          value={query}
          disabled={loading}
          onChange={(e) =>
            setQuery(
              e.target.value
            )
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              void runSearch();
            }
          }}
        />

        <Button
          variant="contained"
          disabled={loading || !query.trim()}
          onClick={runSearch}
        >
          {loading ? "Searching…" : "Search"}
        </Button>

      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {results.map(
        (result, index) => (

          <Paper
            key={index}
            sx={{
              p: 2,
              mb: 2,
              background:
                "#fafafa",
            }}
          >

            <Typography
              variant="subtitle1"
            >
              {result.source}
            </Typography>

            <Typography
              variant="caption"
            >
              Score:
              {" "}
              {result.score.toFixed(4)}
            </Typography>

            <Typography
              sx={{ mt: 1 }}
            >
              {result.text}
            </Typography>

          </Paper>
        )
      )}

    </Paper>
  );
}