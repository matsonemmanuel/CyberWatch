const API_URL = "http://127.0.0.1:5000/api/v1";

export async function getDashboardStats() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/dashboard/stats`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;
}