import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import DeviceList from "../components/DeviceList";

import { getDevices } from "../services/deviceService";

function Devices() {

    const [devices, setDevices] = useState([]);

    useEffect(() => {

        loadDevices();

    }, []);

    async function loadDevices() {

        try {

            const data = await getDevices();

            console.log(data);

            setDevices(data.devices);

        }

        catch (error) {

            console.error(error);

        }

    }

   return (

    <div className="dashboard-container">

        <Sidebar />

        <div className="dashboard-content">

            <Topbar />

            <DeviceList devices={devices} />

        </div>

    </div>

  );

}

export default Devices;