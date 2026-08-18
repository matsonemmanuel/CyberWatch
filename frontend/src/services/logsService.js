const API_URL = "http://127.0.0.1:5000/api/v1";


// =====================================================
// GET RECENT LOGS
// =====================================================

export async function getRecentLogs() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/logs`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;
}


// =====================================================
// GET LOGS
// =====================================================

export async function getLogs(
    search = "",
    severity = "",
    status = "",
    archived = "false",
    page = 1,
    limit = 10
) {

    const token = localStorage.getItem("token");

    const params = new URLSearchParams();


    if (search) {

        params.append(
            "search",
            search
        );

    }


    if (
        severity &&
        severity !== "All"
    ) {

        params.append(
            "severity",
            severity
        );

    }


    if (
        status &&
        status !== "All"
    ) {

        params.append(
            "status",
            status
        );

    }


    if (archived === "archived") {

        params.append(
            "archived",
            "true"
        );

    }


    params.append(
        "page",
        page
    );


    params.append(
        "limit",
        limit
    );


    const response = await fetch(
        `${API_URL}/logs?${params.toString()}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );


    const data = await response.json();

    return data;
}


// =====================================================
// GET SINGLE LOG
// =====================================================

export async function getLog(logId) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/logs/${logId}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );


    const data = await response.json();

    return data;
}


// =====================================================
// UPDATE LOG
// =====================================================

export async function updateLog(
    logId,
    logData
) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/logs/${logId}`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify(logData)
        }
    );


    const data = await response.json();

    return data;
}

// =====================================================
// UPDATE LOG STATUS
// =====================================================

export async function updateLogStatus(
    logId,
    status
) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/logs/${logId}/status`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify({
                status: status
            })
        }
    );


    const data = await response.json();

    return data;
}

// =====================================================
// ARCHIVE LOG
// =====================================================

export async function archiveLog(logId) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/logs/${logId}/archive`,
        {
            method: "PATCH",

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;
}