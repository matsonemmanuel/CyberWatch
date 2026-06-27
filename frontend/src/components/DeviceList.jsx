import "../styles/devicelist.css";
import { useNavigate } from "react-router-dom";

function DeviceList({ devices }) {

    const navigate = useNavigate();

    return (

        <div className="device-list-card">

            <div className="device-header">

                <h2>Registered Devices</h2>

                <span>{devices.length} Devices</span>

            </div>

            <table className="device-table">

                <thead>

                    <tr>

                        <th>Hostname</th>
                        <th>IP Address</th>
                        <th>Operating System</th>
                        <th>Status</th>
                        <th>Registered</th>
                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {devices.length > 0 ? (

                        devices.map((device) => (

                            <tr key={device.id}>

                                <td>{device.hostname}</td>

                                <td>{device.ip_address}</td>

                                <td>{device.operating_system}</td>

                                <td>
                                    <span className={`status-badge ${device.status}`}>
                                        {device.status}
                                    </span>
                                </td>

                                <td>
                                    {new Date(device.registered_at).toLocaleDateString()}
                                </td>

                                <td>

                                    <div className="action-buttons">

                                        <button
                                            className="action-btn view-btn"
                                            title="View Device"
                                            onClick={() => navigate(`/devices/${device.id}`)}
                                        >
                                            👁
                                        </button>

                                        <button
                                            className="action-btn edit-btn"
                                            title="Edit Device"
                                        >
                                            ✏️
                                        </button>

                                        <button
                                            className="action-btn disable-btn"
                                            title={
                                                device.status === "disabled"
                                                    ? "Enable Device"
                                                    : "Disable Device"
                                            }
                                        >
                                            {device.status === "disabled" ? "✅" : "🚫"}
                                        </button>

                                        <button
                                            className="action-btn delete-btn"
                                            title="Delete Device"
                                        >
                                            🗑
                                        </button>

                                    </div>

                                </td>

                            </tr>

                        ))

                    ) : (

                        <tr>

                            <td colSpan="6" style={{ textAlign: "center", padding: "30px" }}>

                                No devices found.

                            </td>

                        </tr>

                    )}

                </tbody>

            </table>

        </div>

    );

}

export default DeviceList;