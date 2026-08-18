const API_URL = "http://127.0.0.1:5000/api/v1";


// =====================================================
// GET ALERTS
// =====================================================

export async function getAlerts(
    severity = "",
    status = ""
) {

    const token = localStorage.getItem("token");

    const params = new URLSearchParams();


    if (severity && severity !== "All") {

        params.append(
            "severity",
            severity
        );

    }


    if (status && status !== "All") {

        params.append(
            "status",
            status
        );

    }


    const response = await fetch(
        `${API_URL}/alerts?${params.toString()}`,
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
// GET SINGLE ALERT
// =====================================================

export async function getAlert(alertId) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/alerts/${alertId}`,
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
// CREATE ALERT
// =====================================================

export async function createAlert(alertData) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/alerts`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify(alertData)
        }
    );


    const data = await response.json();

    return data;
}


// =====================================================
// UPDATE ALERT STATUS
// =====================================================

export async function updateAlertStatus(
    alertId,
    status
) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/alerts/${alertId}/status`,
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