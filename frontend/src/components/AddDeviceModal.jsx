import { useState } from "react";

import "../styles/adddevicemodal.css";
import CustomDropdown from "./CustomDropdown";
import { createDevice } from "../services/deviceService";


function AddDeviceModal({
    isOpen,
    onClose,
    onDeviceAdded
}) {

  const [hostname, setHostname] = useState("");

  async function handleAddDevice() {

    try {

        const deviceData = {

            hostname,

            ip_address: ipAddress,

            operating_system: operatingSystem,

            status

        };

        const result = await createDevice(deviceData);

        if (result.status === "success") {

            setHostname("");
            setIpAddress("");
            setOperatingSystem("");
            setStatus("active");

            onClose();

            onDeviceAdded();

        }

        console.log(result);

    }

    catch (error) {

        console.error(error);

    }

}

  const [ipAddress, setIpAddress] = useState("");

  const [operatingSystem, setOperatingSystem] = useState("");

  const [status, setStatus] = useState("active");

    return (

        <div className="modal-overlay">

            <div className="modal-card">

                <div className="modal-header">

                    <h2>Register New Device</h2>

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
                            placeholder="e.g. Lab-PC-06"
                            value={hostname}
                            onChange={(e) => setHostname(e.target.value)}
                        />

                    </div>

                    <div className="form-group">

                        <label>IP Address</label>

                        <input
                            type="text"
                            placeholder="192.168.1.50"
                            value={ipAddress}
                            onChange={(e) => setIpAddress(e.target.value)}
                        />

                    </div>

                    <div className="form-group">

                        <label>Operating System</label>

                        <input
                            type="text"
                            placeholder="Windows 11"
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

                <div className="modal-footer">

                    <button
                        className="cancel-btn"
                        onClick={onClose}
                    >
                        Cancel
                    </button>

                    <button
                        className="save-btn"
                        onClick={handleAddDevice}
                    >

                        Add Device

                    </button>

                </div>

            </div>

        </div>

    );

}

export default AddDeviceModal;