const API_URL = "http://127.0.0.1:5000/api/v1";


// =========================================================
// GET ALL DEVICES
// =========================================================

export async function getDevices() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices`,
        {
            method: "GET",

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;

}


// =========================================================
// GET SINGLE DEVICE
// =========================================================

export async function getDevice(deviceId) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices/${deviceId}`,
        {
            method: "GET",

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;

}


// =========================================================
// CREATE DEVICE
// =========================================================

export async function createDevice(deviceData) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify(deviceData)
        }
    );

    const data = await response.json();

    return data;

}


// =========================================================
// UPDATE DEVICE
// =========================================================

export async function updateDevice(
    deviceId,
    deviceData
) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices/${deviceId}`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify(deviceData)
        }
    );

    const data = await response.json();

    return data;

}


// =========================================================
// UPDATE DEVICE STATUS
// =========================================================

export async function updateDeviceStatus(
    deviceId,
    status
) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices/${deviceId}/status`,
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


// =========================================================
// DELETE DEVICE
// =========================================================

export async function deleteDevice(deviceId) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/devices/${deviceId}`,
        {
            method: "DELETE",

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    return data;

}