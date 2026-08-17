import cyberwatchLogo from "../assets/cyberwatchlogo-rm.png";
import { NavLink } from "react-router-dom";
import "../styles/sidebar.css";

function Sidebar() {
    return (
        <aside className="sidebar">

            <div className="sidebar-header">
                <img
                    src={cyberwatchLogo}
                    alt="CyberWatch Logo"
                    className="sidebar-logo"
                />
            </div>

            <nav className="sidebar-menu">

                <ul>

                    <li>
                        <NavLink to="/dashboard">
                            <span>🏠</span>
                            <span>Dashboard</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/devices">
                            <span>🖥</span>
                            <span>Devices</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/logs">
                            <span>📋</span>
                            <span>Security Logs</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/alerts">
                            <span>🚨</span>
                            <span>Alerts</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/users">
                            <span>👥</span>
                            <span>Users</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/audit">
                            <span>📝</span>
                            <span>Audit Trail</span>
                        </NavLink>
                    </li>

                    <li>
                        <NavLink to="/settings">
                            <span>⚙</span>
                            <span>Settings</span>
                        </NavLink>
                    </li>

                </ul>

            </nav>

        </aside>
    );
}

export default Sidebar;