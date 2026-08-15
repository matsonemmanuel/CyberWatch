import { useEffect, useState } from "react";

import "../styles/adddevicemodal.css";
import CustomDropdown from "./CustomDropdown";
import { updateDevice } from "../services/deviceService";

function EditDeviceModal({
    isOpen,
    onClose,
    device,
    onDeviceUpdated
}) {
    

const [hostname, setHostname] = useState("");
const [ipAddress, setIpAddress] = useState("");
const [operatingSystem, setOperatingSystem] = useState("");
const [status, setStatus] = useState("active");

const [isSaving, setIsSaving] = useState(false);
const [errorMessage, setErrorMessage] = useState("");

async function handleUpdateDevice() {

    setErrorMessage("");

    setIsSaving(true);

    try {

        const deviceData = {

            hostname,

            ip_address: ipAddress,

            operating_system: operatingSystem,

            status

        };

        const result = await updateDevice(
            device.id,
            deviceData
        );

        console.log(result);

        if (result.status === "success") {

            onClose();

            onDeviceUpdated();

        }

        else {

            setErrorMessage(result.message);

        }

    }

    catch (error) {

        console.error(error);

        setErrorMessage("Unable to update device.");

    }

    finally {

        setIsSaving(false);

    }

}

useEffect(() => {

    if (device) {

        setHostname(device.hostname);
        setIpAddress(device.ip_address);
        setOperatingSystem(device.operating_system);
        setStatus(device.status);

    }

}, [device]);

if (!isOpen) return null;

return (

    <div className="modal-overlay">

        <div className="modal-card">

            <div className="modal-header">

                <h2>Edit Device</h2>

                <button
                    className="close-btn"
                    onClick={onClose}
                >
                    ✕
                </button>

            </div>

            <div className="modal-body">

                <div className="form-group">

                    <label>Hostname</label>

                    <input
                        type="text"
                        value={hostname}
                        onChange={(e) => setHostname(e.target.value)}
                    />

                </div>

                <div className="form-group">

                    <label>IP Address</label>

                    <input
                        type="text"
                        value={ipAddress}
                        onChange={(e) => setIpAddress(e.target.value)}
                    />

                </div>

                <div className="form-group">

                    <label>Operating System</label>

                    <input
                        type="text"
                        value={operatingSystem}
                        onChange={(e) => setOperatingSystem(e.target.value)}
                    />

                </div>

                <div className="form-group">

                    <label>Status</label>

                    <CustomDropdown
                        options={[
                            "active",
                            "offline",
                            "disabled"
                        ]}
                        selected={status}
                        onSelect={setStatus}
                        fullWidth
                    />

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
                    onClick={handleUpdateDevice}
                    disabled={isSaving}
                >
                    {isSaving ? "Saving..." : "Save Changes"}
                </button>

            </div>

        </div>

    </div>

);

}

export default EditDeviceModal;