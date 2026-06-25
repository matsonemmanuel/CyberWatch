import "../styles/recentlogs.css";

function RecentLogs({ logs }) {

    

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

                            <p>{log.device.hostname}</p>

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