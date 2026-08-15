import { BrowserRouter, Routes, Route } from "react-router-dom"

import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Devices from "./pages/Devices";
import DeviceDetails from "./pages/DeviceDetails";
import ProtectedRoute from "./components/ProtectedRoute";
import SecurityLogs from "./pages/SecurityLogs";

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

        <Route
            path="/logs"
            element={
                <ProtectedRoute>
                    <SecurityLogs />
                </ProtectedRoute>
            }
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App