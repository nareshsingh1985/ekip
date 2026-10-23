import { Alert, Button, CircularProgress, Paper, Stack, Typography } from "@mui/material";
import { useState } from "react";
import axios from "axios";
import { getSummary, getRisks, getActions } from "../api/InsightsApi";

type InsightType = "summary" | "risks" | "actions";

const insightLabels: Record<InsightType, string> = {
    summary: "Executive Summary",
    risks: "Risks",
    actions: "Action Items",
};

export default function InsightsPanel() {
    const [output, setOutput] = useState("");
    const [outputType, setOutputType] = useState<InsightType | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const runInsight = async (type: InsightType) => {
        setLoading(true);
        setError(null);
        setOutput("");
        setOutputType(type);

        try {
            const result = type === "summary"
                ? await getSummary()
                : type === "risks"
                    ? await getRisks()
                    : await getActions();
            if (typeof result.result !== "string" || !result.result.trim()) {
                setError("The server returned an empty insight. Please try again.");
                return;
            }
            setOutput(result.result);
        } catch (requestError: unknown) {
            const detail = axios.isAxiosError<{ detail?: string }>(requestError)
                ? requestError.response?.data?.detail
                : undefined;
            setError(
                detail
                ?? (requestError instanceof Error
                    ? requestError.message
                    : "Unable to generate insights. Please try again.")
            );
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
            {output && outputType && (
                <>
                    <Typography variant="subtitle1" component="h3" gutterBottom>
                        {insightLabels[outputType]}
                    </Typography>
                    <Typography sx={{ whiteSpace: "pre-wrap" }}>{output}</Typography>
                </>
            )}
        </Paper>
    );
}