import cyberwatchLogo from "../assets/cyberwatchlogo-rm.png";
import { NavLink } from "react-router-dom";
import "../styles/sidebar.css";


function Sidebar() {

    return (

        <div className="sidebar">

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

                            🏠 Dashboard

                        </NavLink>

                    </li>

                    <li>

                        <NavLink to="/devices">

                            🖥 Devices

                        </NavLink>

                    </li>

                    
                    <NavLink to="/logs">
                        📋 Security Logs
                    </NavLink>

                    <NavLink to="/alerts">
                        🚨 Alerts
                    </NavLink>

                    <NavLink to="/users">
                        👥 Users
                    </NavLink>

                    <NavLink to="/audit">
                        📝 Audit Trail
                    </NavLink>

                    <NavLink to="/settings">
                        ⚙ Settings
                    </NavLink>

                </ul>

            </nav>

        </div>

    );

}

export default Sidebar;