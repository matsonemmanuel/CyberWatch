export async function getLogHistory() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:5000/api/v1/log-history",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;
}