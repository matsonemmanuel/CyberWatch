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

export async function updateDevice(deviceId, deviceData) {

    const token = localStorage.getItem("token");

    const response = await fetch(

        `http://127.0.0.1:5000/api/v1/devices/${deviceId}`,

        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify(deviceData)
        }

    );

    return await response.json();

}

export async function updateDeviceStatus(deviceId, status) {

    const token = localStorage.getItem("token");

    const response = await fetch(

        `http://127.0.0.1:5000/api/v1/devices/${deviceId}/status`,

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

    return await response.json();

}

export async function deleteDevice(deviceId) {

    const token = localStorage.getItem("token");

    const response = await fetch(

        `http://127.0.0.1:5000/api/v1/devices/${deviceId}`,

        {
            method: "DELETE",

            headers: {
                Authorization: `Bearer ${token}`
            }

        }

    );

    return await response.json();

}