
import "../styles/viewlogmodal.css";

function ViewLogModal({ isOpen, log, onClose }) {

    if (!isOpen || !log) {
        return null;
    }

    return (

        <div className="view-log-overlay">

            <div className="view-log-modal">

                <div className="view-log-header">

                    <h2>Security Log Details</h2>

                    <button
                        className="view-log-close"
                        onClick={onClose}
                        title="Close"
                    >
                        ×
                    </button>

                </div>


                <div className="view-log-body">

                    <div className="log-detail">

                        <span className="log-detail-label">
                            Log ID
                        </span>

                        <span className="log-detail-value">
                            #{log.id}
                        </span>

                    </div>


                    <div className="log-detail">

                        <span className="log-detail-label">
                            Event
                        </span>

                        <span className="log-detail-value">
                            {log.event}
                        </span>

                    </div>


                    <div className="log-detail">

                        <span className="log-detail-label">
                            Severity
                        </span>

                        <span
                            className={`severity-badge ${log.severity}`}
                        >
                            {log.severity}
                        </span>

                    </div>


                    <div className="log-detail">

                        <span className="log-detail-label">
                            Status
                        </span>

                        <span className={`log-status ${log.status}`}>
                            {log.status}
                        </span>

                    </div>


                    <div className="log-detail">

                        <span className="log-detail-label">
                            Archived
                        </span>

                        <span className="log-detail-value">
                            {log.archived ? "Yes" : "No"}
                        </span>

                    </div>


                    <div className="log-detail">

                        <span className="log-detail-label">
                            Timestamp
                        </span>

                        <span className="log-detail-value">
                            {new Date(
                                log.timestamp
                            ).toLocaleString()}
                        </span>

                    </div>


                    <div className="view-log-section-title">
                        Device Information
                    </div>


                    {log.device ? (

                        <>

                            <div className="log-detail">

                                <span className="log-detail-label">
                                    Hostname
                                </span>

                                <span className="log-detail-value">
                                    {log.device.hostname}
                                </span>

                            </div>


                            <div className="log-detail">

                                <span className="log-detail-label">
                                    IP Address
                                </span>

                                <span className="log-detail-value">
                                    {log.device.ip_address}
                                </span>

                            </div>


                            <div className="log-detail">

                                <span className="log-detail-label">
                                    Operating System
                                </span>

                                <span className="log-detail-value">
                                    {log.device.operating_system}
                                </span>

                            </div>

                        </>

                    ) : (

                        <div className="no-device">
                            Device information is no longer available.
                        </div>

                    )}

                </div>


                <div className="view-log-footer">

                    <button
                        className="view-log-close-btn"
                        onClick={onClose}
                    >
                        Close
                    </button>

                </div>

            </div>

        </div>

    );

}

export default ViewLogModal;