export async function getDevices() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:5000/api/v1/devices",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;

}

export async function createDevice(deviceData) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:5000/api/v1/devices",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify(deviceData)
        }
    );

    return response.json();

}