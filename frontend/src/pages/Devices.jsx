import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import DeviceToolbar from "../components/DeviceToolbar";
import DeviceList from "../components/DeviceList";
import AddDeviceModal from "../components/AddDeviceModal";
import EditDeviceModal from "../components/EditDeviceModal";
import ConfirmationModal from "../components/ConfirmationModal";

import { getDevices } from "../services/deviceService";

function Devices() {

    const [devices, setDevices] = useState([]);

    const [totalRecords, setTotalRecords] = useState(0);

    const [currentPage, setCurrentPage] = useState(1);

    const [perPage, setPerPage] = useState(10);

    const [searchTerm, setSearchTerm] = useState("");

    const [statusFilter, setStatusFilter] = useState("All");

    const [showAddModal, setShowAddModal] = useState(false);
    

    const [showEditModal, setShowEditModal] = useState(false);

    const [selectedDevice, setSelectedDevice] = useState(null);

    const [showStatusModal, setShowStatusModal] = useState(false);

    const [confirmationAction, setConfirmationAction] = useState("");

    useEffect(() => {

        loadDevices();

    }, []);

    async function loadDevices() {

        try {

            const data = await getDevices();

            console.log("Devices loaded:", data);

            if (data.status === "success") {

                setDevices(data.devices);

                setTotalRecords(data.total_records);

                setCurrentPage(data.page);

                setPerPage(data.per_page);

            } else {

                setDevices([]);

            }

        }

        catch (error) {

            console.error(error);

            setDevices([]);

        }

    }

    function handleEditDevice(device) {

        console.log("Selected Device:", device);

        setSelectedDevice(device);

        setShowEditModal(true);

    }

    function handleToggleDeviceStatus(device) {

        console.log("Selected Device:", device);

        setSelectedDevice(device);

        setConfirmationAction("status");

        setShowStatusModal(true);

    }

    function handleDeleteDevice(device) {

        console.log("Delete Device:", device);

        setSelectedDevice(device);

        setConfirmationAction("delete");

        setShowStatusModal(true);

    }
    /*
        Temporary frontend filtering.

        This will be removed later when
        backend search and pagination are implemented.
    */

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

                    <DeviceList
                        devices={filteredDevices}
                        totalRecords={totalRecords}
                        currentPage={currentPage}
                        perPage={perPage}
                        onEditDevice={handleEditDevice}
                        onToggleDeviceStatus={handleToggleDeviceStatus}
                        onDeleteDevice={handleDeleteDevice}
                    />

                    {showAddModal && (

                        <AddDeviceModal
                            isOpen={showAddModal}
                            onClose={() => setShowAddModal(false)}
                            onDeviceAdded={loadDevices}
                        />

                    )}

                    <EditDeviceModal
                        isOpen={showEditModal}
                        onClose={() => setShowEditModal(false)}
                        device={selectedDevice}
                        onDeviceUpdated={loadDevices}
                    />

                    {showStatusModal && (

                        <ConfirmationModal
                            device={selectedDevice}
                            action={confirmationAction}
                            onClose={() => setShowStatusModal(false)}
                            onStatusUpdated={loadDevices}
                        />

                    )}

                </div>

            </div>

        </div>

    );

}

export default Devices;