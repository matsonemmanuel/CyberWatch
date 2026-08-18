import "../styles/viewdevicemodal.css";


function ViewDeviceModal({
    isOpen,
    device,
    onClose
}) {

    // Do not render anything if modal is closed
    // or there is no selected device.
    if (!isOpen || !device) {

        return null;

    }


    // =========================================
    // CLOSE WHEN CLICKING OUTSIDE MODAL
    // =========================================

    function handleOverlayClick(event) {

        if (event.target === event.currentTarget) {

            onClose();

        }

    }


    return (

        <div
            className="view-device-overlay"
            onClick={handleOverlayClick}
        >

            <div
                className="view-device-modal"
                onClick={(event) =>
                    event.stopPropagation()
                }
            >


                {/* =========================================
                    HEADER
                ========================================= */}

                <div className="view-device-header">

                    <h2>
                        Device Details
                    </h2>

                    <button
                        type="button"
                        className="view-device-close"
                        onClick={onClose}
                        title="Close"
                    >
                        ×
                    </button>

                </div>


                {/* =========================================
                    BODY
                ========================================= */}

                <div className="view-device-body">


                    {/* DEVICE ID */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            Device ID
                        </span>

                        <span className="device-detail-value">
                            #{device.id}
                        </span>

                    </div>


                    {/* HOSTNAME */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            Hostname
                        </span>

                        <span className="device-detail-value">

                            {device.hostname || "N/A"}

                        </span>

                    </div>


                    {/* IP ADDRESS */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            IP Address
                        </span>

                        <span className="device-detail-value">

                            {device.ip_address || "N/A"}

                        </span>

                    </div>


                    {/* OPERATING SYSTEM */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            Operating System
                        </span>

                        <span className="device-detail-value">

                            {device.operating_system || "N/A"}

                        </span>

                    </div>


                    {/* STATUS */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            Status
                        </span>

                        <span
                            className={`status-badge ${
                                device.status || ""
                            }`}
                        >

                            {device.status || "N/A"}

                        </span>

                    </div>


                    {/* REGISTERED */}

                    <div className="device-detail">

                        <span className="device-detail-label">
                            Registered
                        </span>

                        <span className="device-detail-value">

                            {device.registered_at
                                ? new Date(
                                    device.registered_at
                                ).toLocaleString()
                                : "N/A"}

                        </span>

                    </div>


                </div>


                {/* =========================================
                    FOOTER
                ========================================= */}

                <div className="view-device-footer">

                    <button
                        type="button"
                        className="view-device-close-btn"
                        onClick={onClose}
                    >
                        Close
                    </button>

                </div>


            </div>

        </div>

    );

}


export default ViewDeviceModal;