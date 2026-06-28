export async function getDevice(id) {

    const token = localStorage.getItem("token");

    const response = await fetch(

        `http://127.0.0.1:5000/api/v1/devices/${id}`,

        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }

    );

    return response.json();

}