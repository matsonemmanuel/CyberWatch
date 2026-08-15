import "../styles/adddevicemodal.css";
import { useState } from "react";
import {
    updateDeviceStatus,
    deleteDevice
} from "../services/deviceService";

function ConfirmationModal({
    device,
    action,
    onClose,
    onStatusUpdated
}) {

  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleStatusChange() {

    setErrorMessage("");
    setIsSaving(true);

    try {

        let result;

        if (action === "delete") {

            result = await deleteDevice(device.id);

        } else {

            const newStatus =

                device.status === "disabled"

                    ? "active"

                    : "disabled";

            result = await updateDeviceStatus(
                device.id,
                newStatus
            );

        }

        console.log(result);

        if (result.status === "success") {

            onClose();

            onStatusUpdated();

        } else {

            setErrorMessage(result.message);

        }

    } catch (error) {

        console.error(error);

        setErrorMessage("Unable to update device status.");

    } finally {

        setIsSaving(false);

    }

}

    return (

        <div className="modal-overlay">

            <div className="modal-card">

                <div className="modal-header">

                    <h2>

                        {

                            action === "delete"

                                ? "Delete Device"

                                : (

                                    device.status === "disabled"

                                        ? "Enable Device"

                                        : "Disable Device"

                                )

                        }

                    </h2>

                    <button
                        className="close-btn"
                        onClick={onClose}
                    >
                        ✕
                    </button>

                </div>

                <div className="modal-body">

                    <div>

                        <p>

                            Are you sure you want to

                            <strong>

                                {

                                    action === "delete"

                                        ? " delete "

                                        : (

                                            device.status === "disabled"

                                                ? " enable "

                                                : " disable "

                                        )

                                }

                            </strong>

                            this device?

                        </p>

                        <h3>

                            {device.hostname}

                        </h3>

                        <p>

                            {

                                action === "delete"

                                    ? "This device will be removed from the active device list but will remain in the database for audit purposes."

                                    : (

                                        device.status === "disabled"

                                            ? "Monitoring will resume immediately after enabling this device."

                                            : "This device will stop sending monitoring data until it is enabled again."

                                    )

                            }

                        </p>

                      </div>

                </div>

                {errorMessage && (

                    <div className="form-error">

                        {errorMessage}

                    </div>

                )}

                <div className="modal-footer">

                    <button
                        className="cancel-btn"
                        onClick={onClose}
                    >
                        Cancel
                    </button>

                    <button
                        className="save-btn"
                        onClick={handleStatusChange}
                        disabled={isSaving}
                    >
                        {

                            isSaving

                            ? "Saving..."

                            : (

                                action === "delete"

                                    ? "Delete"

                                    : (

                                        device.status === "disabled"

                                            ? "Enable"

                                            : "Disable"

                                    )

                            )

                        }
                    </button>

                </div>

            </div>

        </div>

    );

}

export default ConfirmationModal;