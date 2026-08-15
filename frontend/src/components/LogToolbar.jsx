
function LogToolbar({
    searchTerm,
    setSearchTerm,
    severityFilter,
    setSeverityFilter,
    statusFilter,
    setStatusFilter,
    archivedFilter,
    setArchivedFilter,
    onReset,
}) {



    return (

        <div className="log-toolbar">

            {/* Search */}

            <input
                type="text"
                placeholder="Search logs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />


            {/* Severity */}

            <select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
            >

                <option value="All">All Severity</option>

                <option value="low">Low</option>

                <option value="medium">Medium</option>

                <option value="high">High</option>

            </select>


            {/* Status */}

            <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
            >

                <option value="All">All Status</option>

                <option value="open">Open</option>

                <option value="resolved">Resolved</option>

            </select>


            {/* Archived */}

            <select
                value={archivedFilter}
                onChange={(e) => setArchivedFilter(e.target.value)}
            >

                <option value="active">Active Logs</option>

                <option value="archived">Archived Logs</option>

                <option value="all">All Logs</option>

            </select>

            <button
                className="reset-btn"
                onClick={onReset}
            >
                Reset
            </button>

        </div>

    );

}



export default LogToolbar;