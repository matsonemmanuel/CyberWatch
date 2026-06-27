import "../styles/devicetoolbar.css";

import CustomDropdown from "./CustomDropdown";
import { useState } from "react";


function DeviceToolbar({
    searchTerm,
    setSearchTerm,
    statusFilter,
    setStatusFilter,
    onAddDevice
}) {

    const [selectedStatus, setSelectedStatus] = useState("All Status");

    return (

        <div className="device-toolbar">

            <div className="search-section">

                <input
                    type="text"
                    placeholder="Search hostname or IP address..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />

            </div>

            <div className="toolbar-actions">

                <CustomDropdown
                    options={[
                        "All",
                        "active",
                        "offline",
                        "disabled"
                    ]}
                    selected={statusFilter}
                    onSelect={setStatusFilter}
                />

                <button
                    className="add-device-btn"
                    onClick={onAddDevice}
                >

                    + Add Device

                </button>

            </div>

        </div>

    );

}

export default DeviceToolbar;