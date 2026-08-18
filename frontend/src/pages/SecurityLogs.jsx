import { useEffect, useState } from "react";

import { getLogs, getLog } from "../services/logsService";

import LogList from "../components/LogList";
import ViewLogModal from "../components/ViewLogModal";
import LogToolbar from "../components/LogToolbar";
import EditLogModal from "../components/EditLogModal";

import "../styles/securitylogs.css";


function SecurityLogs() {

    const [logs, setLogs] = useState([]);

    const [searchTerm, setSearchTerm] = useState("");

    const [severityFilter, setSeverityFilter] = useState("All");

    const [statusFilter, setStatusFilter] = useState("All");

    const [archivedFilter, setArchivedFilter] = useState("active");

    const [currentPage, setCurrentPage] = useState(1);

    const [limit, setLimit] = useState(10);

    const [totalLogs, setTotalLogs] = useState(0);

    const [totalPages, setTotalPages] = useState(0);


    /* =====================================================
       VIEW LOG STATE
    ===================================================== */

    const [showViewModal, setShowViewModal] = useState(false);

    const [selectedLog, setSelectedLog] = useState(null);


    /* =====================================================
       EDIT LOG STATE
    ===================================================== */

    const [showEditModal, setShowEditModal] = useState(false);

    const [editLog, setEditLog] = useState(null);


    /* =====================================================
       VIEW LOG
    ===================================================== */

    async function handleViewLog(log) {

        try {

            const data = await getLog(log.id);

            console.log("Log details:", data);

            if (data.status === "success") {

                setSelectedLog(data.data);

                setShowViewModal(true);

            }

        } catch (error) {

            console.error(
                "Failed to load log:",
                error
            );

        }

    }


    /* =====================================================
       EDIT LOG
    ===================================================== */

    async function handleEditLog(log) {

        try {

            const data = await getLog(log.id);

            console.log("Edit log details:", data);

            if (data.status === "success") {

                setEditLog(data.data);

                setShowEditModal(true);

            }

        } catch (error) {

            console.error(
                "Failed to load log for editing:",
                error
            );

        }

    }


    /* =====================================================
       CLOSE EDIT MODAL
    ===================================================== */

    function handleCloseEditModal() {

        setShowEditModal(false);

        setEditLog(null);

    }


    /* =====================================================
       LOG UPDATED
    ===================================================== */

    function handleLogUpdated() {

        setShowEditModal(false);

        setEditLog(null);

        // Reload the logs
        setCurrentPage((page) => page);

    }


    /* =====================================================
       RESET FILTERS
    ===================================================== */

    function handleReset() {

        setSearchTerm("");

        setSeverityFilter("All");

        setStatusFilter("All");

        setArchivedFilter("active");

        setCurrentPage(1);

    }


    /* =====================================================
       LOAD SECURITY LOGS
    ===================================================== */

    useEffect(() => {

        const timer = setTimeout(() => {

            async function loadLogs() {

                try {

                    const data = await getLogs(
                        searchTerm,
                        severityFilter,
                        statusFilter,
                        archivedFilter,
                        currentPage,
                        limit
                    );

                    console.log(
                        "Security Logs:",
                        data
                    );


                    if (data.status === "success") {

                        setLogs(data.logs || []);

                        setTotalLogs(
                            data.total_logs || 0
                        );

                        setTotalPages(
                            data.total_pages || 0
                        );

                    }

                } catch (error) {

                    console.error(
                        "Failed to load logs:",
                        error
                    );

                }

            }

            loadLogs();

        }, 500);


        return () => clearTimeout(timer);

    }, [
        searchTerm,
        severityFilter,
        statusFilter,
        archivedFilter,
        currentPage,
        limit
    ]);


    /* =====================================================
       PAGE
    ===================================================== */

    return (

        <div className="security-logs-page">


            {/* =================================================
               TOOLBAR
            ================================================= */}

            <LogToolbar

                searchTerm={searchTerm}

                setSearchTerm={setSearchTerm}


                severityFilter={severityFilter}

                setSeverityFilter={setSeverityFilter}


                statusFilter={statusFilter}

                setStatusFilter={setStatusFilter}


                archivedFilter={archivedFilter}

                setArchivedFilter={setArchivedFilter}


                onReset={handleReset}

            />


            {/* =================================================
               LOG LIST
            ================================================= */}

            <LogList

                logs={logs}

                totalLogs={totalLogs}

                onViewLog={handleViewLog}

                onEditLog={handleEditLog}

            />


            {/* =================================================
               VIEW LOG MODAL
            ================================================= */}

            <ViewLogModal

                isOpen={showViewModal}

                log={selectedLog}

                onClose={() => {

                    setShowViewModal(false);

                    setSelectedLog(null);

                }}

            />


            {/* =================================================
               EDIT LOG MODAL
            ================================================= */}

            <EditLogModal

                isOpen={showEditModal}

                log={editLog}

                onClose={handleCloseEditModal}

                onLogUpdated={handleLogUpdated}

            />


            {/* =================================================
               PAGINATION
            ================================================= */}

            <div className="pagination">

                <button

                    onClick={() =>
                        setCurrentPage(
                            currentPage - 1
                        )
                    }

                    disabled={
                        currentPage === 1
                    }

                >
                    Previous
                </button>


                <span>

                    Page {currentPage} of {totalPages}

                </span>


                <button

                    onClick={() =>
                        setCurrentPage(
                            currentPage + 1
                        )
                    }

                    disabled={
                        currentPage === totalPages ||
                        totalPages === 0
                    }

                >
                    Next
                </button>

            </div>


        </div>

    );

}


export default SecurityLogs;