# =====================================================
# CYBERWATCH CORRELATION ENGINE
# =====================================================

from datetime import datetime, timezone

from datetime import timedelta

from database.db import get_db_connection


# =====================================================
# RISK SCORES
# =====================================================

EVENT_RISK_SCORES = {

    "Unauthorized USB Device Detected": 2,

    "Multiple Failed Login Attempts": 3,

    "Malicious File Download Detected": 4,

    "Suspicious PowerShell Activity": 3,

    "Unknown Device Connected": 2,

    "Login Outside Normal Hours": 2

}

# =====================================================
# EVENT PATTERNS
# =====================================================

EVENT_PATTERNS = [

    {
        "keywords": [
            "usb"
        ],
        "category": "usb_activity",
        "risk": 2
    },

    {
        "keywords": [
            "failed login"
        ],
        "category": "failed_login",
        "risk": 3
    },

    {
        "keywords": [
            "multiple failed"
        ],
        "category": "failed_login",
        "risk": 3
    },

    {
        "keywords": [
            "malware"
        ],
        "category": "malware",
        "risk": 4
    },

    {
        "keywords": [
            "malicious"
        ],
        "category": "malware",
        "risk": 4
    },

    {
        "keywords": [
            "powershell"
        ],
        "category": "powershell",
        "risk": 3
    },

    {
        "keywords": [
            "unknown device"
        ],
        "category": "unknown_device",
        "risk": 2
    },

    {
        "keywords": [
            "outside normal hours"
        ],
        "category": "unusual_login_time",
        "risk": 2
    },

    {
        "keywords": [
            "after hours"
        ],
        "category": "unusual_login_time",
        "risk": 2
    }

]


# =====================================================
# CALCULATE RISK SCORE
# =====================================================

def calculate_risk_score(logs):

    score = 0

    matched_events = []

    for log in logs:

        event = log.get(
            "event",
            ""
        ).lower()

        matched = False


        # =================================================
        # CHECK EVENT PATTERNS
        # =================================================

        for pattern in EVENT_PATTERNS:

            keywords = pattern["keywords"]

            # All keywords must appear in the event
            if all(
                keyword in event
                for keyword in keywords
            ):

                score += pattern["risk"]

                matched_events.append({

                    "event": log.get("event"),

                    "category": pattern["category"],

                    "risk": pattern["risk"]

                })

                matched = True

                break


        # =================================================
        # FALLBACK TO EXACT EVENT RULE
        # =================================================

        if not matched:

            original_event = log.get(
                "event"
            )

            risk = EVENT_RISK_SCORES.get(
                original_event,
                0
            )

            if risk > 0:

                score += risk

                matched_events.append({

                    "event": original_event,

                    "category": "known_event",

                    "risk": risk

                })


    return {

        "score": score,

        "matched_events": matched_events

    }

# =====================================================
# TIME-BASED CORRELATION
# =====================================================

def detect_time_based_patterns(logs):
    """
    Detect suspicious events that occur close together
    in time on the same device.
    """

    findings = []

    # -------------------------------------------------
    # REQUIRE AT LEAST 2 LOGS
    # -------------------------------------------------

    if len(logs) < 2:
        return findings


    # -------------------------------------------------
    # CONVERT TIMESTAMPS
    # -------------------------------------------------

    parsed_logs = []

    for log in logs:

        timestamp = log.get("timestamp")

        if not timestamp:
            continue

        try:

            parsed_time = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            parsed_logs.append({
                "log": log,
                "time": parsed_time
            })

        except Exception:

            print(
                f"Unable to parse timestamp for log "
                f"{log.get('id')}"
            )


    # -------------------------------------------------
    # SORT LOGS BY TIME
    # -------------------------------------------------

    parsed_logs.sort(
        key=lambda item: item["time"]
    )


    # -------------------------------------------------
    # 10-MINUTE CORRELATION WINDOW
    # -------------------------------------------------

    time_window = timedelta(
        minutes=10
    )


    # -------------------------------------------------
    # CHECK EVENTS OCCURRING CLOSE TOGETHER
    # -------------------------------------------------

    for i in range(len(parsed_logs)):

        first_event = parsed_logs[i]

        nearby_events = []

        for j in range(
            i + 1,
            len(parsed_logs)
        ):

            second_event = parsed_logs[j]

            time_difference = (
                second_event["time"]
                - first_event["time"]
            )


            if time_difference <= time_window:

                nearby_events.append(
                    second_event
                )

            else:

                break


        # -------------------------------------------------
        # 3 OR MORE EVENTS WITHIN 10 MINUTES
        # -------------------------------------------------

        if len(nearby_events) >= 2:

            event_count = (
                len(nearby_events) + 1
            )

            findings.append({

                "type": "time_based_activity",

                "message": (
                    f"{event_count} security events "
                    f"occurred within 10 minutes."
                ),

                "risk": 5

            })

            break


    return findings

# =====================================================
# APPLY CORRELATION RULES
# =====================================================

def apply_correlation_rules(logs, matched_events, current_score):
    """
    Look for relationships between security events
    and increase the risk score when suspicious
    patterns occur together.
    """

    correlation_bonus = 0

    correlation_events = []


    # =================================================
    # COUNT USB EVENTS
    # =================================================

    usb_events = [

        log for log in logs

        if "usb" in log.get(
            "event",
            ""
        ).lower()

    ]


    usb_count = len(usb_events)


    # =================================================
    # RULE 1: REPEATED USB ACTIVITY
    # =================================================

    if usb_count >= 3:

        correlation_bonus += 3

        correlation_events.append({

            "rule": "repeated_usb_activity",

            "message": (
                f"{usb_count} USB-related events "
                "were detected on the same device."
            ),

            "risk": 3

        })


    elif usb_count == 2:

        correlation_bonus += 1

        correlation_events.append({

            "rule": "repeated_usb_activity",

            "message": (
                "Multiple USB-related events "
                "were detected on the same device."
            ),

            "risk": 1

        })

    # =================================================
    # RULE 2: USB + MALWARE CORRELATION
    # =================================================

    malware_events = [

        log for log in logs

        if (
            "malware" in log.get(
                "event",
                ""
            ).lower()

            or

            "malicious" in log.get(
                "event",
                ""
            ).lower()
        )

    ]


    if usb_count > 0 and len(malware_events) > 0:

        correlation_bonus += 5

        correlation_events.append({

            "rule": "usb_malware_correlation",

            "message": (
                "USB activity and malware-related "
                "activity were detected on the same device."
            ),

            "risk": 5

        })

    # =================================================
    # RULE 3: MULTIPLE HIGH-SEVERITY EVENTS
    # =================================================

    high_severity_events = [

        log for log in logs

        if log.get(
            "severity",
            ""
        ).lower() == "high"

    ]


    high_count = len(
        high_severity_events
    )


    if high_count >= 3:

        correlation_bonus += 4

        correlation_events.append({

            "rule": "multiple_high_severity_events",

            "message": (
                f"{high_count} high-severity events "
                "were detected on the same device."
            ),

            "risk": 4

        })


    elif high_count == 2:

        correlation_bonus += 2

        correlation_events.append({

            "rule": "multiple_high_severity_events",

            "message": (
                "Multiple high-severity events "
                "were detected on the same device."
            ),

            "risk": 2

        })

        # =================================================
    # RULE 4: TIME-BASED CORRELATION
    # =================================================

    time_findings = detect_time_based_patterns(
        logs
    )


    for finding in time_findings:

        correlation_bonus += finding["risk"]

        correlation_events.append({

            "rule": finding["type"],

            "message": finding["message"],

            "risk": finding["risk"]

        })


    # =================================================
    # FINAL SCORE
    # =================================================

    final_score = current_score + correlation_bonus


    return {

        "score": final_score,

        "correlation_bonus": correlation_bonus,

        "correlation_events": correlation_events

    }

# =====================================================
# GENERATE CORRELATION ALERT
# =====================================================

def generate_correlation_alert(
    device_id,
    logs,
    risk_result
):
    """
    Generate a security alert when the correlation
    engine determines that a device is at high risk.

    Existing correlation alerts are not duplicated.
    """

    risk_score = risk_result["score"]

    correlation_events = risk_result[
        "correlation_events"
    ]


    # =================================================
    # DETERMINE RISK LEVEL
    # =================================================

    risk_level = determine_risk_level(
        risk_score
    )


    # =================================================
    # ONLY ALERT ON HIGH / CRITICAL RISK
    # =================================================

    if risk_level not in [
        "high",
        "critical"
    ]:

        return {

            "status": "no_alert",

            "message": (
                "Risk level does not require "
                "a correlation alert."
            ),

            "risk_score": risk_score,

            "risk_level": risk_level

        }


    # =================================================
    # BUILD ALERT TITLE
    # =================================================

    alert_title = (
        f"{risk_level.upper()} Correlated Security Risk"
    )


    # =================================================
    # BUILD ALERT MESSAGE
    # =================================================

    messages = [

        event["message"]

        for event in correlation_events

    ]


    if messages:

        alert_message = (
            f"CyberWatch detected a {risk_level} "
            f"correlated security risk on device "
            f"{device_id}. "
            f"Risk score: {risk_score}. "
            + " ".join(messages)
        )

    else:

        alert_message = (
            f"CyberWatch detected a {risk_level} "
            f"security risk on device "
            f"{device_id}. "
            f"Risk score: {risk_score}."
        )


    # =================================================
    # DATABASE CONNECTION
    # =================================================

    connection = get_db_connection()

    cursor = connection.cursor()


    try:

        # =================================================
        # CHECK FOR EXISTING CORRELATION ALERT
        # =================================================

        cursor.execute(
            """
            SELECT
                id,
                status
            FROM alerts
            WHERE device_id = ?
            AND title = ?
            AND status != 'resolved'
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                device_id,
                alert_title
            )
        )


        existing_alert = cursor.fetchone()


        # =================================================
        # EXISTING ALERT / CREATE ALERT
        # =================================================

        if existing_alert:
            alert_id = existing_alert["id"]

            cursor.execute(
                """
                SELECT message, severity, status
                FROM alerts
                WHERE id = ?
                """,
                (alert_id,)
            )
            current_alert = cursor.fetchone()

            if (
                current_alert["message"] == alert_message
                and current_alert["severity"] == risk_level
            ):
                return {
                    "status": "existing",
                    "message": (
                        "Correlation alert already exists "
                        "and is up to date."
                    ),
                    "alert_id": alert_id,
                    "risk_score": risk_score,
                    "risk_level": risk_level
                }

            cursor.execute(
                """
                UPDATE alerts
                SET log_id = ?, message = ?, severity = ?
                WHERE id = ?
                """,
                (logs[0]["id"], alert_message, risk_level, alert_id)
            )
            connection.commit()

            return {
                "status": "updated",
                "message": "Existing correlation alert was updated successfully.",
                "alert_id": alert_id,
                "risk_score": risk_score,
                "risk_level": risk_level
            }

        created_at = datetime.now(
            timezone.utc
        ).isoformat().replace(
            "+00:00",
            "Z"
        )


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
                logs[0]["id"],
                device_id,
                alert_title,
                alert_message,
                risk_level,
                "active",
                created_at
            )
        )


        alert_id = cursor.lastrowid


        connection.commit()


        print(
            f"Correlation alert created "
            f"for device {device_id}."
        )


        return {

            "status": "created",

            "message": (
                "Correlation alert created successfully."
            ),

            "alert_id": alert_id,

            "risk_score": risk_score,

            "risk_level": risk_level

        }


    except Exception as error:

        connection.rollback()


        print(
            "Error generating correlation alert:",
            error
        )


        return {

            "status": "error",

            "message": (
                "Failed to generate correlation alert."
            ),

            "error": str(error)

        }


    finally:

        connection.close()

# =====================================================
# DETERMINE RISK LEVEL
# =====================================================

def determine_risk_level(score):

    if score >= 10:

        return "critical"

    elif score >= 7:

        return "high"

    elif score >= 4:

        return "medium"

    else:

        return "low"


# =====================================================
# GET RECENT LOGS FOR DEVICE
# =====================================================

def get_device_logs(device_id, limit=20):
    """
    Retrieve recent security logs belonging
    to a specific device.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

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
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                device_id,
                limit
            )
        )

        rows = cursor.fetchall()

        logs = []

        for row in rows:

            logs.append({

                "id": row["id"],

                "device_id": row["device_id"],

                "event": row["event"],

                "severity": row["severity"],

                "status": row["status"],

                "archived": row["archived"],

                "timestamp": row["timestamp"]

            })

        return logs

    finally:

        connection.close()

# =================================================
# TEST 3: CORRELATE REAL DEVICE LOGS
# =================================================

print(
    "\nFetching real logs for Device 1..."
)

device_logs = get_device_logs(
    device_id=1,
    limit=20
)

print(
    f"Logs found: {len(device_logs)}"
)

# =================================================
# TIME-BASED CORRELATION TEST
# =================================================

time_findings = detect_time_based_patterns(
    device_logs
)

print(
    "\nTime-Based Correlation Findings:"
)

for finding in time_findings:

    print(
        f"- {finding['message']} "
        f"(+{finding['risk']})"
    )

for log in device_logs:

    print(
        f"- Log {log['id']}: "
        f"{log['event']} "
        f"(severity: {log['severity']})"
    )

print(
    "\nCalculating risk for Device 1..."
)

device_risk = calculate_risk_score(
    device_logs
)

# =================================================
# APPLY CORRELATION RULES
# =================================================

correlated_risk = apply_correlation_rules(
    device_logs,
    device_risk["matched_events"],
    device_risk["score"]
)

device_risk_level = determine_risk_level(
    correlated_risk["score"]
)

# =================================================
# GENERATE CORRELATION ALERT
# =================================================

correlation_alert = generate_correlation_alert(
    device_id=1,
    logs=device_logs,
    risk_result=correlated_risk
)

print(
    "\nCorrelation Alert Result:"
)

print(
    correlation_alert
)

print(
    "\nDevice 1 Risk Score:",
    correlated_risk["score"]
)



print(
    "Device 1 Risk Level:",
    device_risk_level
)

print(
    "\nDetected Security Patterns:"
)

for event in device_risk["matched_events"]:

    print(
        f"- {event['event']} "
        f"→ {event['category']} "
        f"(+{event['risk']})"
    )

print(
    "\nCorrelation Findings:"
)

if correlated_risk["correlation_events"]:

    for correlation in correlated_risk[
        "correlation_events"
    ]:

        print(
            f"- {correlation['message']} "
            f"(+{correlation['risk']})"
        )

else:

    print(
        "- No correlation patterns detected."
    )
# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    test_logs = [

        {
            "device_id": 1,
            "event": "Unknown Device Connected"
        },

        {
            "device_id": 1,
            "event": "Multiple Failed Login Attempts"
        },

        {
            "device_id": 1,
            "event": "Suspicious PowerShell Activity"
        },

        {
            "device_id": 1,
            "event": "Malicious File Download Detected"
        }

    ]


    result = calculate_risk_score(
        test_logs
    )


    risk_level = determine_risk_level(
        result["score"]
    )


    print("\n========================================")
    print("CYBERWATCH CORRELATION ENGINE")
    print("========================================\n")

    print(
        "Risk Score:",
        result["score"]
    )

    print(
        "Risk Level:",
        risk_level
    )

    print(
        "\nMatched Events:"
    )

    for event in result["matched_events"]:

        print(
            f"- {event['event']} "
            f"(+{event['risk']})"
        )

