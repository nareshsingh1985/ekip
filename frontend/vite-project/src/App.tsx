import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Layout from "./components/Layout";

import DashboardPage from "./pages/DashboardPage";
import SearchPage from "./pages/SearchPage";
import DocumentsPage from "./pages/DocumentsPage";
import InsightsPage from "./pages/InsightsPage";
import GraphPage from "./pages/GraphPage";
import AssistantPage from "./pages/AssistantPage";

export default function App() {

  return (

    <BrowserRouter>

      <Layout>

        <Routes>

          <Route
            path="/"
            element={<DashboardPage />}
          />

          <Route
            path="/search"
            element={<SearchPage />}
          />

          <Route
            path="/documents"
            element={<DocumentsPage />}
          />

          <Route
            path="/insights"
            element={<InsightsPage />}
          />

          <Route
            path="/graph"
            element={<GraphPage />}
          />

          <Route
            path="/assistant"
            element={<AssistantPage />}
          />

        </Routes>

      </Layout>

    </BrowserRouter>
  );
}