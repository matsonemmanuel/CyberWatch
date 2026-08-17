function LogList({ logs, totalLogs }) {

    return (

        <div className="log-list-card">

            <div className="log-header">

                <h2>Security Logs</h2>

                <span>
                    Total Logs: {totalLogs ?? logs.length}
                </span>

            </div>


            <div className="log-table-container">

                <table className="log-table">

                    <thead>

                        <tr>

                            <th>ID</th>
                            <th>Event</th>
                            <th>Severity</th>
                            <th>Status</th>
                            <th>Device</th>
                            <th>Timestamp</th>
                            <th>Actions</th>

                        </tr>

                    </thead>


                    <tbody>

                        {logs.length > 0 ? (

                            logs.map((log) => (

                                <tr key={log.id}>

                                    <td>{log.id}</td>

                                    <td>{log.event}</td>

                                    <td>

                                        <span
                                            className={`severity-badge ${log.severity}`}
                                        >
                                            {log.severity}
                                        </span>

                                    </td>

                                    <td>

                                        <span
                                            className={`log-status ${log.status}`}
                                        >
                                            {log.status}
                                        </span>

                                    </td>

                                    <td>

                                        {log.device
                                            ? log.device.hostname
                                            : "Unknown Device"}

                                    </td>

                                    <td>

                                        {new Date(
                                            log.timestamp
                                        ).toLocaleString()}

                                    </td>

                                    <td>

                                        <div className="action-buttons">

                                            <button
                                                className="action-btn view-btn"
                                                title="View Log"
                                            >
                                                👁
                                            </button>

                                            <button
                                                className="action-btn edit-btn"
                                                title="Edit Log"
                                            >
                                                ✏️
                                            </button>

                                            <button
                                                className="action-btn disable-btn"
                                                title="Change Status"
                                            >
                                                🔄
                                            </button>

                                            <button
                                                className="action-btn delete-btn"
                                                title="Archive Log"
                                            >
                                                📦
                                            </button>

                                        </div>

                                    </td>

                                </tr>

                            ))

                        ) : (

                            <tr>

                                <td
                                    colSpan="7"
                                    className="empty-logs"
                                >
                                    No security logs found.
                                </td>

                            </tr>

                        )}

                    </tbody>

                </table>

            </div>

        </div>

    );

}


export default LogList;