
from datetime import (
    datetime,
    timezone
)

from database.db import get_db_connection

from utils.logger import log_activity

   # Register Device Service

def register_device_service(
    user_id,
    username,
    data
):
    """
    Register a new device in CyberWatch.
    """

    hostname = data.get("hostname")
    ip_address = data.get("ip_address")
    operating_system = data.get("operating_system")
    status = data.get("status", "active")

    if not hostname or not ip_address or not operating_system or not status:

        return {
            "status": "error",
            "message": "All fields are required"
        }, 400
    

    timestamp = datetime.now(
        timezone.utc
    ).isoformat().replace('+00:00', 'Z')

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
    '''
    INSERT INTO devices
    (
        hostname,
        ip_address,
        operating_system,
        status,
        registered_at
    )
    VALUES (?, ?, ?, ?, ?)
    ''',
    (
        hostname,
        ip_address,
        operating_system,
        status,
        timestamp
    )
)
    
    connection.commit()

    device_id = cursor.lastrowid

    log_activity(
    user_id,
    username,
    f"Registered device {hostname}"
)
    
    connection.close()

    return {
        "status": "success",
        "message": "Device registered successfully",
        "data": {
            "id": device_id,
            "hostname": hostname,
            "ip_address": ip_address,
            "operating_system": operating_system,
            "status": status,
            "registered_at": timestamp
        }
    }, 201

    # Retrieve All Devices Service

def get_devices_service(search):
    """
    Retrieve all devices with optional search filtering.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
    """
    SELECT *
    FROM devices
    WHERE
        hostname LIKE ?
        OR ip_address LIKE ?
        OR operating_system LIKE ?
        OR status LIKE ?
    """,
    (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    )
)
    
    rows = cursor.fetchall()

    connection.close()

    devices = []

    for row in rows:

        devices.append({
            "id": row["id"],
            "hostname": row["hostname"],
            "ip_address": row["ip_address"],
            "operating_system": row["operating_system"],
            "status": row["status"],
            "registered_at": row["registered_at"]
        })

    return {
        "status": "success",
        "total_devices": len(devices),
        "devices": devices
    }, 200

    # Retrieve Single Device Service

def get_device_service(device_id):
    """
    Retrieve a single device by its ID.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        """,
        (device_id,)
    )

    row = cursor.fetchone()

    connection.close()
    
    if not row:

      return {
          "status": "error",
          "message": "Device not found"
      }, 404
    
    device = {
        "id": row["id"],
        "hostname": row["hostname"],
        "ip_address": row["ip_address"],
        "operating_system": row["operating_system"],
        "status": row["status"],
        "registered_at": row["registered_at"]
    }

    return {
        "status": "success",
        "device": device
    }, 200



# Update Device Status Service

def update_device_status_service(
    device_id,
    data
):
    """
    Update the status of a device.
    """

    status = data.get("status")

    allowed_statuses = [
        "active",
        "offline",
        "maintenance",
        "disabled"
    ]

    # Validate status
    if status not in allowed_statuses:

        return {
            "status": "error",
            "message": "Invalid device status"
        }, 400

    # Connect to database
    connection = get_db_connection()

    cursor = connection.cursor()

    # Check if the device exists
    cursor.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        """,
        (device_id,)
    )

    device = cursor.fetchone()

    if not device:

        connection.close()

        return {
            "status": "error",
            "message": "Device not found"
        }, 404

    # Update device status
    cursor.execute(
        """
        UPDATE devices
        SET status = ?
        WHERE id = ?
        """,
        (status, device_id)
    )

    connection.commit()

    # Retrieve the updated device
    cursor.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        """,
        (device_id,)
    )

    updated_device = cursor.fetchone()

    connection.close()

    return {
        "status": "success",
        "message": "Device status updated successfully",
        "data": {
            "id": updated_device["id"],
            "hostname": updated_device["hostname"],
            "status": updated_device["status"]
        }
    }, 200


  # Retrieve Device Logs Service

def get_device_logs_service(device_id):
    """
    Retrieve all logs for a specific device.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    # Verify device exists
    cursor.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        """,
        (device_id,)
    )

    device = cursor.fetchone()

    if not device:

        connection.close()

        return {
            "status": "error",
            "message": "Device not found"
        }, 404
    
    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE device_id = ?
        """,
        (device_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    logs = []

    for row in rows:

        logs.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "event": row["event"],
            "severity": row["severity"],
            "status": row["status"],
            "archived": bool(row["archived"])
        })

        return {
            "status": "success",
            "device_id": device_id,
            "total_logs": len(logs),
            "logs": logs
        }, 200