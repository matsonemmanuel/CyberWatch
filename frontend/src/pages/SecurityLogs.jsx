import { useEffect, useState } from "react";

import { getLogs } from "../services/logsService";

import LogList from "../components/LogList";
import LogToolbar from "../components/LogToolbar";

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


    function handleReset() {

        setSearchTerm("");
        setSeverityFilter("All");
        setStatusFilter("All");
        setArchivedFilter("active");
        setCurrentPage(1);

    }


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

                    console.log("Security Logs:", data);

                    if (data.status === "success") {

                        setLogs(data.logs);

                        setTotalLogs(data.total_logs);

                        setTotalPages(data.total_pages);

                    }

                } catch (error) {

                    console.error("Failed to load logs:", error);

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


    return (

        <div className="security-logs-page">

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


            <LogList
                logs={logs}
                totalLogs={totalLogs}
            />


            <div className="pagination">

                <button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                >
                    Previous
                </button>


                <span>
                    Page {currentPage} of {totalPages}
                </span>


                <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>

            </div>

        </div>

    );

}


export default SecurityLogs;