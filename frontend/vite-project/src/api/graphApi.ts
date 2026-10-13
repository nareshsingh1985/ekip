import api from "./client";

export interface GraphNode {
  id: string;
  label: string;
  group: string;
}

export interface GraphLink {
  source: string;
  target: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphLink[];
}

export const getGraph =
  async (): Promise<GraphData> => {

    const response =
      await api.get("/graph");

    return response.data;
  };