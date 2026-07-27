import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Console from "./pages/Console";
import Snapshots from "./pages/Snapshots";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Redirect root to dashboard */}
        <Route
          path="/"
          element={<Navigate to="/dashboard" replace />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/console"
          element={<Console />}
        />

        <Route
          path="/snapshots"
          element={<Snapshots />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;