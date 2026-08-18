import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Devices from "./pages/Devices";
import DeviceDetails from "./pages/DeviceDetails";
import SecurityLogs from "./pages/SecurityLogs";

import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./layouts/DashboardLayout";
import History from "./pages/History";
import Alerts from "./pages/Alerts";


function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* LOGIN */}

                <Route
                    path="/"
                    element={<Login />}
                />


                {/* PROTECTED DASHBOARD AREA */}

                <Route
                    element={
                        <ProtectedRoute>
                            <DashboardLayout />
                        </ProtectedRoute>
                    }
                >

                    <Route
                        path="/dashboard"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/devices"
                        element={<Devices />}
                    />

                    <Route
                        path="/devices/:id"
                        element={<DeviceDetails />}
                    />

                    <Route
                        path="/logs"
                        element={<SecurityLogs />}
                    />

                    <Route
                        path="/history"
                        element={<History />}
                    />

                    <Route
                        path="/alerts"
                        element={<Alerts />}
                    />

                </Route>

            </Routes>

        </BrowserRouter>

    );

}

export default App;