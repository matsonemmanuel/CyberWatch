import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import StatCard from "../components/Statcard";
import RecentLogs from "../components/RecentLogs";
import "../styles/dashboard.css";

function Dashboard() {

    return (

        <div className="dashboard-container">

            <Sidebar />

            <div className="dashboard-content">

                <Topbar />

                <div className="stats-grid">

                  <StatCard
                      icon="🖥"
                      title="Devices"
                      value="18"
                  />

                  <StatCard
                      icon="🚨"
                      title="Alerts"
                      value="4"
                  />

                  <StatCard
                      icon="📋"
                      title="Logs"
                      value="235"
                  />

                  <StatCard
                      icon="👥"
                      title="Users"
                      value="8"
                  />

              </div>

              <RecentLogs />

            </div>

        </div>

    );

}

export default Dashboard;