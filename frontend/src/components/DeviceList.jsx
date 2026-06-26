import "../styles/devicelist.css";

function DeviceList({ devices }) {

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

                    </tr>

                </thead>

                <tbody>

                    {devices.map((device) => (

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

                                {new Date(
                                    device.registered_at
                                ).toLocaleDateString()}

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default DeviceList;