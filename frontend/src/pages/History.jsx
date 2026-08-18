import { useEffect, useState } from "react";

import { getLogHistory } from "../services/logHistoryService";

import "../styles/history.css";


function History() {

    const [history, setHistory] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    /* =====================================================
       LOAD LOG HISTORY
       ===================================================== */

    async function loadHistory() {

        try {

            setLoading(true);

            setError("");


            const data = await getLogHistory();

            console.log("Log History:", data);


            if (data.status === "success") {

                setHistory(data.history || []);

            } else {

                setError(
                    data.message || "Failed to load history"
                );

            }


        } catch (error) {

            console.error(
                "Failed to load log history:",
                error
            );

            setError(
                "Unable to connect to the server."
            );

        } finally {

            setLoading(false);

        }

    }


    /* =====================================================
       LOAD WHEN PAGE OPENS
       ===================================================== */

    useEffect(() => {

        loadHistory();

    }, []);


    /* =====================================================
       REFRESH
       ===================================================== */

    function handleRefresh() {

        loadHistory();

    }


    /* =====================================================
       FORMAT DATE
       ===================================================== */

    function formatDate(dateString) {

        if (!dateString) {
            return "—";
        }


        const date = new Date(dateString);


        if (Number.isNaN(date.getTime())) {
            return dateString;
        }


        return date.toLocaleString();

    }


    /* =====================================================
       RENDER
       ===================================================== */

    return (

        <div className="history-page">


            {/* =================================================
               PAGE HEADER
               ================================================= */}

            <div className="history-page-header">

                <div>

                    <h1>
                        Security History
                    </h1>

                    <p>
                        Track changes made to security logs.
                    </p>

                </div>


                <div className="history-total-card">

                    <span>
                        Total Changes
                    </span>

                    <strong>
                        {history.length}
                    </strong>

                </div>

            </div>



            {/* =================================================
               HISTORY CARD
               ================================================= */}

            <div className="history-card">


                {/* CARD HEADER */}

                <div className="history-card-header">

                    <div>

                        <h2>
                            Log Change History
                        </h2>

                        <p>
                            Audit trail of security log modifications
                        </p>

                    </div>


                    <button
                        className="history-refresh-btn"
                        onClick={handleRefresh}
                        disabled={loading}
                    >

                        ↻ Refresh

                    </button>

                </div>



                {/* =================================================
                   LOADING
                   ================================================= */}

                {loading && (

                    <div className="history-state">

                        <div className="history-spinner"></div>

                        <p>
                            Loading history...
                        </p>

                    </div>

                )}



                {/* =================================================
                   ERROR
                   ================================================= */}

                {!loading && error && (

                    <div className="history-error">

                        <p>
                            {error}
                        </p>

                        <button
                            onClick={handleRefresh}
                        >
                            Try Again
                        </button>

                    </div>

                )}



                {/* =================================================
                   EMPTY STATE
                   ================================================= */}

                {!loading &&
                 !error &&
                 history.length === 0 && (

                    <div className="history-state">

                        <div className="history-empty-icon">
                            ✓
                        </div>

                        <h3>
                            No Changes Yet
                        </h3>

                        <p>
                            No security log modifications
                            have been recorded.
                        </p>

                    </div>

                )}



                {/* =================================================
                   HISTORY TABLE
                   ================================================= */}

                {!loading &&
                 !error &&
                 history.length > 0 && (

                    <div className="history-table-container">

                        <table className="history-table">

                            <thead>

                                <tr>

                                    <th>
                                        HISTORY ID
                                    </th>

                                    <th>
                                        LOG
                                    </th>

                                    <th>
                                        CHANGED BY
                                    </th>

                                    <th>
                                        FIELD
                                    </th>

                                    <th>
                                        CHANGE
                                    </th>

                                    <th>
                                        REASON
                                    </th>

                                    <th>
                                        DATE
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {history.map((item) => (

                                    <tr key={item.id}>


                                        {/* HISTORY ID */}

                                        <td>

                                            <span className="history-id">
                                                #{item.id}
                                            </span>

                                        </td>



                                        {/* LOG */}

                                        <td>

                                            <span className="history-log-badge">

                                                Log #{item.log_id}

                                            </span>

                                        </td>



                                        {/* CHANGED BY */}

                                        <td>

                                            <div className="history-user">

                                                <span className="history-user-avatar">

                                                    {item.username
                                                        ? item.username
                                                            .charAt(0)
                                                            .toUpperCase()
                                                        : "?"}

                                                </span>


                                                <span>
                                                    {item.username || "Unknown"}
                                                </span>

                                            </div>

                                        </td>



                                        {/* FIELD */}

                                        <td>

                                            <span className="history-field-badge">

                                                {item.field_name}

                                            </span>

                                        </td>



                                        {/* CHANGE */}

                                        <td>

                                            <div className="history-change">

                                                <span className="history-old-value">

                                                    {item.old_value || "—"}

                                                </span>


                                                <span className="history-arrow">
                                                    →
                                                </span>


                                                <span className="history-new-value">

                                                    {item.new_value || "—"}

                                                </span>

                                            </div>

                                        </td>



                                        {/* REASON */}

                                        <td>

                                            <span className="history-reason">

                                                {item.reason || "—"}

                                            </span>

                                        </td>



                                        {/* DATE */}

                                        <td>

                                            <span className="history-date">

                                                {formatDate(
                                                    item.created_at
                                                )}

                                            </span>

                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>

        </div>

    );

}


export default History;