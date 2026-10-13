import Button from "@mui/material/Button";
import {
  Alert,
  CircularProgress,
  Paper,
  Typography,
} from "@mui/material";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import ForceGraph2D from "react-force-graph-2d";
import { getGraph } from "../api/graphApi";
import type { GraphData } from "../api/graphApi";

export default function KnowledgeGraph() {
  const [graph, setGraph] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadGraph = useCallback(async () => {
    try {
      const data = await getGraph();
      setGraph(data);
    } catch {
      setError("Unable to load the knowledge graph.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void Promise.resolve().then(loadGraph);
  }, [loadGraph]);

  const refreshGraph = () => {
    setLoading(true);
    setError(null);
    void loadGraph();
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>

      <Typography
        variant="h6"
        gutterBottom
      >
        Knowledge Graph
      </Typography>

      {loading && !graph && <CircularProgress aria-label="Loading knowledge graph" />}
      {error && <Alert severity="error">{error}</Alert>}
      {graph && (
        <>
          <ForceGraph2D
            graphData={{ nodes: graph.nodes, links: graph.edges }}
            width={900}
            height={500}
            nodeColor={(node) => {
              switch (node.group) {
                case "project":
                  return "#1976d2";
                case "risk":
                  return "#d32f2f";
                case "action":
                  return "#388e3c";
                case "team":
                  return "#f57c00";
                default:
                  return "#757575";
              }
            }}
          />
          <Button
            variant="contained"
            sx={{ mt: 2 }}
            disabled={loading}
            onClick={refreshGraph}
          >
            {loading ? "Refreshing…" : "Refresh Graph"}
          </Button>
        </>
      )}
      {error && !graph && (
        <Button
          variant="contained"
          sx={{ mt: 2 }}
          onClick={refreshGraph}
        >
          Retry
        </Button>
      )}

    </Paper>
  );
}