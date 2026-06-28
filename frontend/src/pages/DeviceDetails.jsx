import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getDevice } from "../services/deviceDetailsService";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

import "../styles/devicedetails.css";

function DeviceDetails() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [device, setDevice] = useState(null);

    useEffect(() => {

    async function fetchDevice() {

        const response = await getDevice(id);

        console.log(response);

        if (response.status === "success") {

            setDevice(response.device);

        }

    }

    fetchDevice();

}, [id]);

if (!device) {

    return <p>Loading device...</p>;

}

    return (

        <div className="dashboard-container">

            <Sidebar />

            <div className="dashboard-content">

                <Topbar />

                <div className="device-details-page">

                    <div className="details-header">

                        <button
                            className="back-btn"
                            onClick={() => navigate("/devices")}
                        >
                            ← Back to Devices
                        </button>

                        <h1>Device Information</h1>

                    </div>

                    <div className="device-info-card">

                        <div className="info-row">

                            <span>Hostname</span>

                            <strong>{device.hostname}</strong>

                        </div>

                        <div className="info-row">

                            <span>IP Address</span>

                            <strong>{device.ip_address}</strong>

                        </div>

                        <div className="info-row">

                            <span>Operating System</span>

                            <strong>{device.operating_system}</strong>

                        </div>

                        <div className="info-row">

                            <span>Status</span>

                            <strong>{device.status}</strong>

                        </div>

                        <div className="info-row">

                            <span>Registered</span>

                            <strong>{device.registered_at}</strong>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default DeviceDetails;