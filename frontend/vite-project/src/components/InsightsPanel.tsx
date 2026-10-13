import { Alert, Button, CircularProgress, Paper, Stack, Typography } from "@mui/material";
import { useState } from "react";
import { getSummary, getRisks, getActions } from "../api/InsightsApi";

type InsightType = "summary" | "risks" | "actions";

export default function InsightsPanel() {
    const [output, setOutput] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const runInsight = async (type: InsightType) => {
        setLoading(true);
        setError(null);
        setOutput("");

        try {
            const result = type === "summary"
                ? await getSummary()
                : type === "risks"
                    ? await getRisks()
                    : await getActions();
            setOutput(result.result);
        } catch {
            setError("Unable to generate insights. Please try again.");
        } finally {
            setLoading(false);
        }
    };
    return (
        <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" component="h2" gutterBottom>
                Executive Insights
            </Typography>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 3 }}>
                <Button variant="contained" disabled={loading} onClick={() => runInsight("summary")}>
                    Executive Summary
                </Button>
                <Button variant="contained" color="warning" disabled={loading} onClick={() => runInsight("risks")}>
                    Risks
                </Button>
                <Button variant="contained" color="success" disabled={loading} onClick={() => runInsight("actions")}>
                    Action Items
                </Button>
            </Stack>
            {loading && <CircularProgress aria-label="Generating insights" />}
            {error && <Alert severity="error">{error}</Alert>}
            {output && <Typography sx={{ whiteSpace: "pre-wrap" }}>{output}</Typography>}
        </Paper>
    );
}