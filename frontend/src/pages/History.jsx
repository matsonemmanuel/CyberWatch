import { useEffect, useState } from "react";

import { getLogHistory } from "../services/logHistoryService";

import "../styles/history.css";


function History() {

    const [history, setHistory] = useState([]);

    const [total, setTotal] = useState(0);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    // =====================================================
    // LOAD HISTORY
    // =====================================================

    async function loadHistory() {

        setLoading(true);

        setError("");

        try {

            const data = await getLogHistory();

            console.log("Log History:", data);


            if (data.status === "success") {

                setHistory(data.history || []);

                setTotal(data.total || 0);

            } else {

                setError(
                    data.message ||
                    "Failed to load log history."
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


    // =====================================================
    // LOAD ON PAGE OPEN
    // =====================================================

    useEffect(() => {

        loadHistory();

    }, []);


    // =====================================================
    // FORMAT DATE
    // =====================================================

    function formatDate(timestamp) {

        if (!timestamp) {
            return "N/A";
        }

        return new Date(timestamp).toLocaleString();

    }


    // =====================================================
    // PAGE
    // =====================================================

    return (

        <div className="history-page">


            {/* =================================================
               HEADER
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


                <div className="history-total">

                    <span>
                        Total Changes
                    </span>

                    <strong>
                        {total}
                    </strong>

                </div>

            </div>


            {/* =================================================
               HISTORY CARD
            ================================================= */}

            <div className="history-card">


                {/* =================================================
                   CARD HEADER
                ================================================= */}

                <div className="history-card-header">

                    <div>

                        <h2>
                            Log Change History
                        </h2>

                        <span>
                            Audit trail of security log modifications
                        </span>

                    </div>


                    <button
                        className="history-refresh-btn"
                        onClick={loadHistory}
                        disabled={loading}
                    >
                        {loading
                            ? "Loading..."
                            : "↻ Refresh"}
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

                        <strong>
                            Unable to load history
                        </strong>

                        <span>
                            {error}
                        </span>

                        <button
                            onClick={loadHistory}
                        >
                            Try Again
                        </button>

                    </div>

                )}


                {/* =================================================
                   EMPTY
                ================================================= */}

                {!loading &&
                    !error &&
                    history.length === 0 && (

                        <div className="history-state">

                            <div className="history-empty-icon">
                                ✓
                            </div>

                            <h3>
                                No History Yet
                            </h3>

                            <p>
                                Changes made to security logs
                                will appear here.
                            </p>

                        </div>

                    )}


                {/* =================================================
                   TABLE
                ================================================= */}

                {!loading &&
                    !error &&
                    history.length > 0 && (

                        <div className="history-table-container">

                            <table className="history-table">

                                <thead>

                                    <tr>

                                        <th>
                                            History ID
                                        </th>

                                        <th>
                                            Log
                                        </th>

                                        <th>
                                            Changed By
                                        </th>

                                        <th>
                                            Field
                                        </th>

                                        <th>
                                            Change
                                        </th>

                                        <th>
                                            Reason
                                        </th>

                                        <th>
                                            Date
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {history.map(
                                        (item) => (

                                            <tr
                                                key={item.id}
                                            >

                                                {/* HISTORY ID */}

                                                <td>

                                                    <span className="history-id">
                                                        #{item.id}
                                                    </span>

                                                </td>


                                                {/* LOG ID */}

                                                <td>

                                                    <span className="history-log-id">
                                                        Log #{item.log_id}
                                                    </span>

                                                </td>


                                                {/* USER */}

                                                <td>

                                                    <div className="history-user">

                                                        <div className="history-user-avatar">
                                                            {item.username
                                                                ? item.username
                                                                    .charAt(0)
                                                                    .toUpperCase()
                                                                : "?"}
                                                        </div>

                                                        <span>
                                                            {item.username ||
                                                                "Unknown"}
                                                        </span>

                                                    </div>

                                                </td>


                                                {/* FIELD */}

                                                <td>

                                                    <span className="history-field">

                                                        {item.field_name}

                                                    </span>

                                                </td>


                                                {/* CHANGE */}

                                                <td>

                                                    <div className="history-change">

                                                        <span className="history-old-value">

                                                            {item.old_value ||
                                                                "N/A"}

                                                        </span>

                                                        <span className="history-arrow">
                                                            →
                                                        </span>

                                                        <span className="history-new-value">

                                                            {item.new_value ||
                                                                "N/A"}

                                                        </span>

                                                    </div>

                                                </td>


                                                {/* REASON */}

                                                <td>

                                                    <div className="history-reason">

                                                        {item.reason}

                                                    </div>

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

                                        )
                                    )}

                                </tbody>

                            </table>

                        </div>

                    )}

            </div>

        </div>

    );

}


export default History;