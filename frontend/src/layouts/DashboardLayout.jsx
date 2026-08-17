import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

import "../styles/dashboard-layout.css";


function DashboardLayout() {
    return (
        <div className="dashboard-layout">

            {/* LEFT SIDEBAR */}
            <aside className="dashboard-sidebar">
                <Sidebar />
            </aside>


            {/* RIGHT SIDE */}
            <section className="dashboard-main">

                {/* TOPBAR */}
                <header className="dashboard-topbar">
                    <Topbar />
                </header>


                {/* PAGE CONTENT */}
                <main className="dashboard-page-content">
                    <Outlet />
                </main>

            </section>

        </div>
    );
}


export default DashboardLayout;