import "../styles/sidebar.css";

function Sidebar() {

    return (

        <div className="sidebar">

            <div className="sidebar-header">

                <h2>CyberWatch</h2>

                <p>- Monitor.Detect.Protect -</p>

            </div>

            <nav className="sidebar-menu">

                <ul>

                    <li className="active">
                        🏠 Dashboard
                    </li>

                    <li>
                        🖥 Devices
                    </li>

                    <li>
                        📋 Security Logs
                    </li>

                    <li>
                        🚨 Alerts
                    </li>

                    <li>
                        👥 Users
                    </li>

                    <li>
                        📝 Audit Trail
                    </li>

                    <li>
                        ⚙ Settings
                    </li>

                </ul>

            </nav>

        </div>

    );

}

export default Sidebar;