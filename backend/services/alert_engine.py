# =====================================================
# CYBERWATCH ALERT ENGINE
# =====================================================

from database.db import get_db_connection
from datetime import datetime, timezone


# =====================================================
# ANALYZE SINGLE LOG
# =====================================================

def analyze_log(log):
    """
    Analyze a security log and determine
    whether an alert should be generated.
    """

    event_raw = log.get(
        "event",
        ""
    )

    event = event_raw.lower()

    severity = log.get(
        "severity",
        ""
    ).lower()


    # =================================================
    # RULE 1: UNAUTHORIZED USB DEVICE
    # =================================================

    if (
        "unauthorized usb" in event
        or "unknown usb" in event
        or "usb device detected" in event
    ):

        return {

            "should_alert": True,

            "title": "Unauthorized USB Device",

            "message": (
                "An unauthorized USB device was detected "
                "on a monitored device."
            ),

            "severity": "high"

        }


    # =================================================
    # RULE 2: MULTIPLE FAILED LOGIN ATTEMPTS
    # =================================================

    if (
        "failed login" in event
        or "multiple failed login" in event
        or "repeated login failure" in event
    ):

        return {

            "should_alert": True,

            "title": "Multiple Failed Login Attempts",

            "message": (
                "Multiple failed login attempts were "
                "detected on a monitored device. "
                "This may indicate a possible "
                "brute-force or unauthorized access attempt."
            ),

            "severity": "high"

        }


    # =================================================
    # RULE 3: MALICIOUS FILE OR DOWNLOAD
    # =================================================

    if (
        "malicious file" in event
        or "malicious download" in event
        or "malware detected" in event
        or "suspicious download" in event
    ):

        return {

            "should_alert": True,

            "title": "Potentially Malicious File Activity",

            "message": (
                "Potentially malicious file or download "
                "activity was detected on a monitored device."
            ),

            "severity": "high"

        }


    # =================================================
    # RULE 4: SUSPICIOUS POWERSHELL / PROCESS
    # =================================================

    if (
        "suspicious powershell" in event
        or "suspicious process" in event
        or "malicious process" in event
    ):

        return {

            "should_alert": True,

            "title": "Suspicious Process Activity",

            "message": (
                "Suspicious process activity was detected "
                "on a monitored device."
            ),

            "severity": "high"

        }


    # =================================================
    # RULE 5: UNKNOWN DEVICE
    # =================================================

    if (
        "unknown device" in event
        or "unrecognized device" in event
        or "new device connected" in event
    ):

        return {

            "should_alert": True,

            "title": "Unknown Device Detected",

            "message": (
                "An unknown or unrecognized device was "
                "detected on the monitored network."
            ),

            "severity": "medium"

        }


    # =================================================
    # RULE 6: UNUSUAL LOGIN TIME
    # =================================================

    if (
        "outside normal hours" in event
        or "unusual login time" in event
        or "after hours login" in event
    ):

        return {

            "should_alert": True,

            "title": "Unusual Login Activity",

            "message": (
                "A login occurred outside the expected "
                "normal activity period."
            ),

            "severity": "medium"

        }


    # =================================================
    # RULE 7: HIGH SEVERITY FALLBACK
    # =================================================

    if severity == "high":

        return {

            "should_alert": True,

            "title": f"High Severity: {event_raw}",

            "message": (
                "A high-severity security event was "
                "detected on a monitored device: "
                f"{event_raw}."
            ),

            "severity": "high"

        }


    # =================================================
    # NO ALERT
    # =================================================

    return {

        "should_alert": False

    }
# =====================================================
# SCAN EXISTING LOGS
# =====================================================

def scan_existing_logs():
    """
    Scan existing security logs and automatically
    create alerts for logs that require attention.

    Existing alerts are not duplicated.
    """

    connection = get_db_connection()

    cursor = connection.cursor()


    try:

        # =================================================
        # GET EXISTING SECURITY LOGS
        # =================================================

        cursor.execute(
            """
            SELECT
                id,
                device_id,
                event,
                severity,
                status,
                archived,
                timestamp
            FROM logs
            ORDER BY id ASC
            """
        )


        logs = cursor.fetchall()


        alerts_created = 0

        alerts_skipped = 0

        logs_checked = 0


        # =================================================
        # ANALYZE EACH LOG
        # =================================================

        for row in logs:

            logs_checked += 1


            log = {

                "id": row["id"],

                "device_id": row["device_id"],

                "event": row["event"],

                "severity": row["severity"],

                "status": row["status"],

                "archived": row["archived"],

                "timestamp": row["timestamp"]

            }


            # =================================================
            # ANALYZE LOG
            # =================================================

            alert_decision = analyze_log(
                log
            )


            # =================================================
            # NO ALERT REQUIRED
            # =================================================

            if not alert_decision["should_alert"]:

                continue


            # =================================================
            # CHECK FOR EXISTING ALERT
            # =================================================

            cursor.execute(
                """
                SELECT id
                FROM alerts
                WHERE log_id = ?
                """,
                (
                    row["id"],
                )
            )


            existing_alert = cursor.fetchone()


            # =================================================
            # ALERT ALREADY EXISTS
            # =================================================

            if existing_alert:

                alerts_skipped += 1

                print(
                    f"Alert already exists for log "
                    f"{row['id']} - skipped."
                )

                continue


            # =================================================
            # CREATE TIMESTAMP
            # =================================================

            created_at = datetime.now(
                timezone.utc
            ).isoformat().replace(
                "+00:00",
                "Z"
            )


            # =================================================
            # CREATE ALERT
            # =================================================

            cursor.execute(
                """
                INSERT INTO alerts
                (
                    log_id,
                    device_id,
                    title,
                    message,
                    severity,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    row["device_id"],
                    alert_decision["title"],
                    alert_decision["message"],
                    alert_decision["severity"],
                    "active",
                    created_at
                )
            )


            alerts_created += 1


            print(
                f"Automatic alert created for "
                f"existing log {row['id']}."
            )


        # =================================================
        # COMMIT CHANGES
        # =================================================

        connection.commit()


        # =================================================
        # RETURN SCAN SUMMARY
        # =================================================

        return {

            "status": "success",

            "message": "Existing logs scanned successfully",

            "logs_checked": logs_checked,

            "alerts_created": alerts_created,

            "alerts_skipped": alerts_skipped

        }


    except Exception as error:

        connection.rollback()


        print(
            "Error scanning existing logs:",
            error
        )


        return {

            "status": "error",

            "message": "Failed to scan existing logs",

            "error": str(error)

        }


    finally:

        connection.close()


# =====================================================
# TEST ALERT ENGINE
# =====================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "CYBERWATCH ALERT ENGINE"
    )

    print(
        "========================================\n"
    )


    # =================================================
    # TEST 1: ANALYZE SAMPLE LOG
    # =================================================

    test_log = {

        "id": 2,

        "device_id": 1,

        "event": "Login Outside Normal Hours",

        "severity": "medium"

    }


    result = analyze_log(
        test_log
    )


    print(
        "Single Log Analysis:"
    )

    print(
        result
    )


    # =================================================
    # TEST 2: SCAN DATABASE
    # =================================================

    print(
        "\nScanning existing logs...\n"
    )


    scan_result = scan_existing_logs()


    print(
        "\nScan Result:"
    )

    print(
        scan_result
    )