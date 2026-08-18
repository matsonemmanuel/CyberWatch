import { useEffect, useState } from "react";

import DeviceToolbar from "../components/DeviceToolbar";
import DeviceList from "../components/DeviceList";
import AddDeviceModal from "../components/AddDeviceModal";
import EditDeviceModal from "../components/EditDeviceModal";
import ConfirmationModal from "../components/ConfirmationModal";
import ViewDeviceModal from "../components/ViewDeviceModal";

import {
    getDevices,
    getDevice
} from "../services/deviceService";

import "../styles/devices.css";


function Devices() {

    const [devices, setDevices] = useState([]);

    const [totalRecords, setTotalRecords] = useState(0);

    const [currentPage, setCurrentPage] = useState(1);

    const [perPage, setPerPage] = useState(10);

    const [searchTerm, setSearchTerm] = useState("");

    const [statusFilter, setStatusFilter] = useState("All");

    const [showAddModal, setShowAddModal] = useState(false);

    const [showEditModal, setShowEditModal] = useState(false);

    const [showViewModal, setShowViewModal] = useState(false);

    const [showStatusModal, setShowStatusModal] = useState(false);

    const [selectedDevice, setSelectedDevice] = useState(null);

    const [confirmationAction, setConfirmationAction] = useState("");


    // =========================================
    // LOAD DEVICES
    // =========================================

    useEffect(() => {

        loadDevices();

    }, []);


    async function loadDevices() {

        try {

            const data = await getDevices();

            console.log("Devices loaded:", data);

            if (data.status === "success") {

                setDevices(data.devices || []);

                setTotalRecords(data.total_records || 0);

                setCurrentPage(data.page || 1);

                setPerPage(data.per_page || 10);

            } else {

                setDevices([]);

                setTotalRecords(0);

            }

        } catch (error) {

            console.error(
                "Failed to load devices:",
                error
            );

            setDevices([]);

            setTotalRecords(0);

        }

    }


    // =========================================
    // VIEW DEVICE
    // =========================================

    async function handleViewDevice(device) {

        // Close other modals first
        setShowEditModal(false);

        setShowStatusModal(false);

        // Clear previous selected device
        setSelectedDevice(null);

        try {

            const data = await getDevice(device.id);

            console.log("Device details:", data);

            if (data.status === "success") {

                /*
                 * IMPORTANT:
                 *
                 * Backend returns:
                 *
                 * {
                 *     status: "success",
                 *     message: "...",
                 *     device: {...}
                 * }
                 *
                 * Therefore we use data.device
                 * and NOT data.data.
                 */

                setSelectedDevice(data.device);

                setShowViewModal(true);

            } else {

                console.error(
                    "Failed to retrieve device:",
                    data.message
                );

            }

        } catch (error) {

            console.error(
                "Failed to load device:",
                error
            );

        }

    }


    // =========================================
    // CLOSE VIEW DEVICE
    // =========================================

    function handleCloseView() {

        setShowViewModal(false);

        setSelectedDevice(null);

    }


    // =========================================
    // EDIT DEVICE
    // =========================================

    function handleEditDevice(device) {

        // Make sure View modal is closed
        setShowViewModal(false);

        // Make sure confirmation modal is closed
        setShowStatusModal(false);

        // Select device
        setSelectedDevice(device);

        // Open Edit modal
        setShowEditModal(true);

    }


    // =========================================
    // CLOSE EDIT DEVICE
    // =========================================

    function handleCloseEdit() {

        setShowEditModal(false);

        setSelectedDevice(null);

    }


    // =========================================
    // CHANGE DEVICE STATUS
    // =========================================

    function handleToggleDeviceStatus(device) {

        // Close other modals
        setShowViewModal(false);

        setShowEditModal(false);

        // Select device
        setSelectedDevice(device);

        // Set confirmation action
        setConfirmationAction("status");

        // Open confirmation modal
        setShowStatusModal(true);

    }


    // =========================================
    // DELETE DEVICE
    // =========================================

    function handleDeleteDevice(device) {

        // Close other modals
        setShowViewModal(false);

        setShowEditModal(false);

        // Select device
        setSelectedDevice(device);

        // Set confirmation action
        setConfirmationAction("delete");

        // Open confirmation modal
        setShowStatusModal(true);

    }


    // =========================================
    // CLOSE CONFIRMATION MODAL
    // =========================================

    function handleCloseStatusModal() {

        setShowStatusModal(false);

        setSelectedDevice(null);

        setConfirmationAction("");

    }


    // =========================================
    // FILTER DEVICES
    // =========================================

    const filteredDevices = devices.filter((device) => {

        const search =
            searchTerm
                .toLowerCase()
                .trim();

        const hostname =
            (device.hostname || "")
                .toLowerCase();

        const ipAddress =
            (device.ip_address || "")
                .toLowerCase();

        const matchesSearch =
            hostname.includes(search) ||
            ipAddress.includes(search);

        const matchesStatus =
            statusFilter === "All" ||
            device.status === statusFilter;

        return (
            matchesSearch &&
            matchesStatus
        );

    });


    // =========================================
    // RENDER
    // =========================================

    return (

        <div className="devices-page">


            {/* =========================================
                DEVICE TOOLBAR
            ========================================= */}

            <DeviceToolbar

                searchTerm={searchTerm}

                setSearchTerm={setSearchTerm}

                statusFilter={statusFilter}

                setStatusFilter={setStatusFilter}

                onAddDevice={() =>
                    setShowAddModal(true)
                }

            />


            {/* =========================================
                DEVICE LIST
            ========================================= */}

            <DeviceList

                devices={filteredDevices}

                totalRecords={totalRecords}

                currentPage={currentPage}

                perPage={perPage}

                onViewDevice={handleViewDevice}

                onEditDevice={handleEditDevice}

                onToggleDeviceStatus={
                    handleToggleDeviceStatus
                }

                onDeleteDevice={
                    handleDeleteDevice
                }

            />


            {/* =========================================
                ADD DEVICE MODAL
            ========================================= */}

            {showAddModal && (

                <AddDeviceModal

                    isOpen={showAddModal}

                    onClose={() => {

                        setShowAddModal(false);

                    }}

                    onDeviceAdded={() => {

                        setShowAddModal(false);

                        loadDevices();

                    }}

                />

            )}


            {/* =========================================
                VIEW DEVICE MODAL
            ========================================= */}

            <ViewDeviceModal

                isOpen={showViewModal}

                device={selectedDevice}

                onClose={handleCloseView}

            />


            {/* =========================================
                EDIT DEVICE MODAL
            ========================================= */}

            <EditDeviceModal

                isOpen={showEditModal}

                onClose={handleCloseEdit}

                device={selectedDevice}

                onDeviceUpdated={() => {

                    setShowEditModal(false);

                    setSelectedDevice(null);

                    loadDevices();

                }}

            />


            {/* =========================================
                STATUS / DELETE CONFIRMATION
            ========================================= */}

            {showStatusModal && (

                <ConfirmationModal

                    device={selectedDevice}

                    action={confirmationAction}

                    onClose={handleCloseStatusModal}

                    onStatusUpdated={() => {

                        setShowStatusModal(false);

                        setSelectedDevice(null);

                        setConfirmationAction("");

                        loadDevices();

                    }}

                />

            )}

        </div>

    );

}


export default Devices;