import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import StatCard from "../components/Statcard";
import RecentLogs from "../components/RecentLogs";
import { getRecentLogs } from "../services/logsService";

import { useState, useEffect } from "react";

import { getDashboardStats } from "../services/dashboardService";

import "../styles/dashboard.css";

function Dashboard() {

    const [stats, setStats] = useState(null);
    const [logs, setLogs] = useState([]);

    useEffect(() => {

    async function loadDashboard() {

    try {

        const statsData = await getDashboardStats();

        setStats(statsData);

        const logsData = await getRecentLogs();

        console.log(logsData);

        setLogs(logsData.logs);

    } catch (error) {

        console.error(error);

    }

}

    loadDashboard();

}, []);

    return (

        <div className="dashboard-container">

            <Sidebar />

            <div className="dashboard-content">

                <Topbar />

                <div className="stats-grid">

                    <StatCard
                        icon="🖥"
                        title="Devices"
                        value={stats?.total_devices}
                    />

                    <StatCard
                        icon="🚨"
                        title="Open Alerts"
                        value={stats?.open_incidents}
                    />

                    <StatCard
                        icon="📋"
                        title="Logs"
                        value={stats?.total_logs}
                    />

                    <StatCard
                        icon="🔥"
                        title="High Severity"
                        value={stats?.high_severity_incidents}
                    />

                </div>
   
    
              <RecentLogs logs={logs} />

            </div>

        </div>

    );

}

export default Dashboard;