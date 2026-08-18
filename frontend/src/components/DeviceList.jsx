import "../styles/devicelist.css";

function DeviceList({
    devices,
    totalRecords,
    currentPage,
    perPage,
    onViewDevice,
    onEditDevice,
    onToggleDeviceStatus,
    onDeleteDevice
}) {

    const firstRecord =
        devices.length > 0
            ? ((currentPage - 1) * perPage) + 1
            : 0;

    const lastRecord =
        Math.min(
            currentPage * perPage,
            totalRecords
        );

    return (
        <div className="device-list-card">

            {/* =========================================
                REGISTERED DEVICES HEADER
            ========================================= */}

            <div className="device-header">

                <h2>Registered Devices</h2>

                <span>
                    Showing {firstRecord} - {lastRecord} of {totalRecords} Devices
                </span>

            </div>


            {/* =========================================
                TABLE ONLY SCROLLS INSIDE THIS AREA
            ========================================= */}

            <div className="device-table-scroll">

                <div className="device-table-container">

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

                                        <td>
                                            {device.hostname}
                                        </td>

                                        <td>
                                            {device.ip_address}
                                        </td>

                                        <td>
                                            {device.operating_system}
                                        </td>

                                        <td>

                                            <span
                                                className={`status-badge ${device.status}`}
                                            >
                                                {device.status}
                                            </span>

                                        </td>

                                        <td>

                                            {new Date(
                                                device.registered_at
                                            ).toLocaleDateString()}

                                        </td>

                                        <td>

                                            <div className="action-buttons">

                                                {/* =========================
                                                    VIEW DEVICE
                                                ========================== */}

                                                <button
                                                    className="action-btn view-btn"
                                                    title="View Device"
                                                    onClick={() =>
                                                        onViewDevice(device)
                                                    }
                                                >
                                                    👁
                                                </button>


                                                {/* =========================
                                                    EDIT DEVICE
                                                ========================== */}

                                                <button
                                                    className="action-btn edit-btn"
                                                    title="Edit Device"
                                                    onClick={() =>
                                                        onEditDevice(device)
                                                    }
                                                >
                                                    ✏️
                                                </button>


                                                {/* =========================
                                                    ENABLE / DISABLE DEVICE
                                                ========================== */}

                                                <button
                                                    className="action-btn disable-btn"
                                                    title={
                                                        device.status === "disabled"
                                                            ? "Enable Device"
                                                            : "Disable Device"
                                                    }
                                                    onClick={() =>
                                                        onToggleDeviceStatus(device)
                                                    }
                                                >
                                                    {device.status === "disabled"
                                                        ? "✅"
                                                        : "🚫"}
                                                </button>


                                                {/* =========================
                                                    DELETE DEVICE
                                                ========================== */}

                                                <button
                                                    className="action-btn delete-btn"
                                                    title="Delete Device"
                                                    onClick={() =>
                                                        onDeleteDevice(device)
                                                    }
                                                >
                                                    🗑
                                                </button>

                                            </div>

                                        </td>

                                    </tr>

                                ))

                            ) : (

                                <tr>

                                    <td
                                        colSpan="6"
                                        className="no-devices"
                                    >
                                        No devices found.
                                    </td>

                                </tr>

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

export default DeviceList;