import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import DeviceToolbar from "../components/DeviceToolbar";
import DeviceList from "../components/DeviceList";
import AddDeviceModal from "../components/AddDeviceModal";

import { getDevices } from "../services/deviceService";

function Devices() {

    const [devices, setDevices] = useState([]);

    const [searchTerm, setSearchTerm] = useState("");

    const [statusFilter, setStatusFilter] = useState("All");

    const [showAddModal, setShowAddModal] = useState(false);

    useEffect(() => {

        loadDevices();

    }, []);

    async function loadDevices() {

        try {

            const data = await getDevices();

            console.log(data);

            setDevices(data.devices);

        }

        catch (error) {

            console.error(error);

        }

    }

    const filteredDevices = devices.filter((device) => {

    const search = searchTerm.toLowerCase();

    const matchesSearch =

        device.hostname.toLowerCase().includes(search) ||

        device.ip_address.toLowerCase().includes(search);

    const matchesStatus =

        statusFilter === "All" ||

        device.status === statusFilter;

    return matchesSearch && matchesStatus;

    });

   return (

    <div className="dashboard-container">

        <Sidebar />

        <div className="dashboard-content">

            <Topbar />

            <div className="devices-content">

               <DeviceToolbar
                    searchTerm={searchTerm}
                    setSearchTerm={setSearchTerm}
                    statusFilter={statusFilter}
                    setStatusFilter={setStatusFilter}
                    onAddDevice={() => setShowAddModal(true)}
                />

                <DeviceList devices={filteredDevices} />

                {showAddModal && (

                    <AddDeviceModal
                        isOpen={showAddModal}
                        onClose={() => setShowAddModal(false)}
                        onDeviceAdded={loadDevices}
                    />

                )}

            </div>

        </div>

    </div>

  );
}

export default Devices;