import "../styles/topbar.css";
function Topbar() {

    return (

        <div className="topbar">

            <div className="topbar-left">

                <h1>CyberWatch Dashboard</h1>

                <p>
                    Security Operations Center
                </p>

            </div>

            <div className="topbar-right">

                <div className="status">

                    🟢 System Healthy

                </div>

                <div className="admin">

                    👤 Admin

                </div>

            </div>

        </div>

    );

}

export default Topbar;