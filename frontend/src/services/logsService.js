export async function getRecentLogs() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:5000/api/v1/logs",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;

}

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
        params.append("search", search);
    }

    if (severity && severity !== "All") {
        params.append("severity", severity);
    }

    if (status && status !== "All") {
        params.append("status", status);
    }

    if (archived === "archived") {
        params.append("archived", "true");
    }

    params.append("page", page);

    params.append("limit", limit);

    const response = await fetch(
        `http://127.0.0.1:5000/api/v1/logs?${params.toString()}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;
}