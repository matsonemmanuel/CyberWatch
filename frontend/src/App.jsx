import { BrowserRouter, Routes, Route } from "react-router-dom"

import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Devices from "./pages/Devices";
import DeviceDetails from "./pages/DeviceDetails";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

  

        <Route
            path="/dashboard"
            element={
                <ProtectedRoute>
                    <Dashboard />
                </ProtectedRoute>
            }
        />

        <Route
            path="/devices"
            element={
                <ProtectedRoute>
                    <Devices />
                </ProtectedRoute>
            }
        />

        <Route
            path="/devices/:id"
            element={
                <ProtectedRoute>
                    <DeviceDetails />
                </ProtectedRoute>
            }
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App