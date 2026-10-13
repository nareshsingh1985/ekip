import { Alert, Box, CircularProgress, Grid, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import StatCard from "./StatCard";
import { getDashboardStats } from "../api/dashboardApi";
import type { DashboardStats } from "../api/dashboardApi";

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let isMounted = true;

        const loadStats = async () => {
            try {
                const data = await getDashboardStats();
                if (isMounted) {
                    setStats(data);
                }
            } catch {
                if (isMounted) {
                    setError("Unable to load dashboard statistics.");
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        void loadStats();

        return () => {
            isMounted = false;
        };
    }, []);

    if (loading) {
        return <CircularProgress aria-label="Loading dashboard statistics" />;
    }

    if (error) {
        return <Alert severity="error" sx={{ mb: 4 }}>{error}</Alert>;
    }

    if (!stats) {
        return null;
    }

    return (
        <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h3" gutterBottom>
                Executive Dashboard
            </Typography>
            <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <StatCard title="Documents Indexed" value={stats.documents} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <StatCard title="Vector Count" value={stats.vectors} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <StatCard title="Collection" value={stats.collection} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <StatCard title="Platform Status" value={stats.status} />
                </Grid>
            </Grid>
        </Box>
    );
}