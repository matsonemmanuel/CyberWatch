import StatCard from "../components/Statcard";
import RecentLogs from "../components/RecentLogs";

import { getRecentLogs } from "../services/logsService";
import { getDashboardStats } from "../services/dashboardService";

import { useState, useEffect } from "react";

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

                setLogs(logsData.logs || []);

            } catch (error) {

                console.error("Dashboard loading error:", error);

            }

        }


        loadDashboard();

    }, []);


    return (

        <div className="dashboard-page">

            {/* ================================
                SUMMARY STATISTICS
            ================================= */}

            <div className="stats-grid">

                <StatCard
                    icon="🖥"
                    title="Devices"
                    value={stats?.total_devices ?? 0}
                />

                <StatCard
                    icon="🚨"
                    title="Open Alerts"
                    value={stats?.open_incidents ?? 0}
                />

                <StatCard
                    icon="📋"
                    title="Logs"
                    value={stats?.total_logs ?? 0}
                />

                <StatCard
                    icon="🔥"
                    title="High Severity"
                    value={stats?.high_severity_incidents ?? 0}
                />

            </div>


            {/* ================================
                RECENT SECURITY EVENTS
            ================================= */}

            <div className="recent-logs-section">

                <RecentLogs logs={logs} />

            </div>

        </div>

    );

}


export default Dashboard;