function ViewAlertModal({
    isOpen,
    alert,
    onClose
}) {

    if (!isOpen || !alert) {
        return null;
    }


    return (

        <div className="alert-modal-overlay">

            <div className="alert-modal">


                {/* =====================================================
                    HEADER
                ===================================================== */}

                <div className="alert-modal-header">

                    <h2>
                        Alert Details
                    </h2>

                    <button
                        type="button"
                        className="alert-modal-close"
                        onClick={onClose}
                    >
                        ×
                    </button>

                </div>


                {/* =====================================================
                    ALERT INFORMATION
                ===================================================== */}

                <div className="alert-modal-body">


                    <div className="alert-detail-row">

                        <strong>
                            Alert ID
                        </strong>

                        <span>
                            {alert.id}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Title
                        </strong>

                        <span>
                            {alert.title}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Message
                        </strong>

                        <span>
                            {alert.message}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Severity
                        </strong>

                        <span
                            className={`alert-severity ${alert.severity}`}
                        >
                            {alert.severity}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Status
                        </strong>

                        <span
                            className={`alert-status ${alert.status}`}
                        >
                            {alert.status}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Log ID
                        </strong>

                        <span>
                            {alert.log_id}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Device ID
                        </strong>

                        <span>
                            {alert.device_id ?? "Unknown"}
                        </span>

                    </div>


                    <div className="alert-detail-row">

                        <strong>
                            Created At
                        </strong>

                        <span>
                            {new Date(
                                alert.created_at
                            ).toLocaleString()}
                        </span>

                    </div>


                </div>


                {/* =====================================================
                    FOOTER
                ===================================================== */}

                <div className="alert-modal-footer">

                    <button
                        type="button"
                        className="alert-modal-close-btn"
                        onClick={onClose}
                    >
                        Close
                    </button>

                </div>


            </div>

        </div>

    );

}


export default ViewAlertModal;