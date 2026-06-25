import "../styles/recentlogs.css";

function RecentLogs() {

    const logs = [

        {
            id: 1,
            event: "USB Device Inserted",
            device: "LAB-PC-07",
            severity: "Medium"
        },

        {
            id: 2,
            event: "Multiple Failed Logins",
            device: "OFFICE-PC-02",
            severity: "High"
        },

        {
            id: 3,
            event: "Firewall Disabled",
            device: "LAB-PC-11",
            severity: "Critical"
        },

        {
            id: 4,
            event: "Malware Detected",
            device: "SERVER-01",
            severity: "Critical"
        }

    ];

    return (

        <div className="recent-logs">

            <h2>Recent Security Events</h2>

            {
                logs.map((log) => (

                    <div
                        key={log.id}
                        className="log-item"
                    >

                        <div>

                            <h4>{log.event}</h4>

                            <p>{log.device}</p>

                        </div>

                        <span className={`severity ${log.severity.toLowerCase()}`}>

                            {log.severity}

                        </span>

                    </div>

                ))
            }

        </div>

    );

}

export default RecentLogs;