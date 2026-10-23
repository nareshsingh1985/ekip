import Button from "@mui/material/Button";
import {
  Alert,
  Box,
  CircularProgress,
  Paper,
  Typography,
} from "@mui/material";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import axios from "axios";
import ForceGraph2D from "react-force-graph-2d";
import { getGraph } from "../api/graphApi";
import type { GraphData } from "../api/graphApi";

export default function KnowledgeGraph() {
  const [graph, setGraph] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [width, setWidth] = useState(0);
  const graphContainer = useRef<HTMLDivElement>(null);

  const loadGraph = useCallback(async () => {
    try {
      const data = await getGraph();
      setGraph(data);
      setError(null);
    } catch (requestError: unknown) {
      const detail = axios.isAxiosError<{ detail?: string }>(requestError)
        ? requestError.response?.data?.detail
        : undefined;
      setError(
        detail
        ?? (requestError instanceof Error
          ? requestError.message
          : "Unable to load the knowledge graph.")
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void Promise.resolve().then(loadGraph);
  }, [loadGraph]);

  useEffect(() => {
    const container = graphContainer.current;
    if (!container) {
      return;
    }

    const observer = new ResizeObserver(([entry]) => {
      setWidth(Math.floor(entry.contentRect.width));
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, [graph?.nodes.length]);

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
          {graph.nodes.length === 0 ? (
            <Alert severity="info">
              No entities were found in the indexed documents. Upload relevant documents and refresh the graph.
            </Alert>
          ) : (
            <Box
              ref={graphContainer}
              sx={{ width: "100%", minHeight: 400, overflow: "hidden" }}
              aria-label="Knowledge graph visualization"
            >
              {width > 0 && (
                <ForceGraph2D
                  graphData={{ nodes: graph.nodes, links: graph.edges }}
                  width={width}
                  height={500}
                  nodeLabel="label"
                  linkLabel="label"
                  linkDirectionalArrowLength={4}
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
                      case "application":
                        return "#7b1fa2";
                      default:
                        return "#757575";
                    }
                  }}
                />
              )}
            </Box>
          )}
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
      {error && (
        <Button
          variant="contained"
          sx={{ mt: 2 }}
          disabled={loading}
          onClick={refreshGraph}
        >
          {loading ? "Loading…" : "Retry"}
        </Button>
      )}

    </Paper>
  );
}