import { useEffect, useState } from "react";

import "../styles/editlogmodal.css";

import CustomDropdown from "./CustomDropdown";

import { updateLog } from "../services/logsService";


function EditLogModal({
    isOpen,
    log,
    onClose,
    onLogUpdated
}) {

    const [severity, setSeverity] = useState("low");

    const [comment, setComment] = useState("");

    const [isSaving, setIsSaving] = useState(false);

    const [errorMessage, setErrorMessage] = useState("");


    /* =====================================================
       LOAD SELECTED LOG
    ===================================================== */

    useEffect(() => {

        if (!log) {
            return;
        }

        setSeverity(
            log.severity || "low"
        );

        setComment(
            ""
        );

        setErrorMessage("");

    }, [log]);


    /* =====================================================
       UPDATE LOG
    ===================================================== */

    async function handleUpdateLog() {

        setErrorMessage("");

        if (!severity) {

            setErrorMessage(
                "Severity is required."
            );

            return;

        }


        if (!comment.trim()) {

            setErrorMessage(
                "Please provide a reason for editing this log."
            );

            return;

        }


        setIsSaving(true);


        try {

            const logData = {

                severity: severity,

                comment: comment.trim()

            };


            console.log(
                "Updating log:",
                logData
            );


            const result = await updateLog(
                log.id,
                logData
            );


            console.log(
                "Update log result:",
                result
            );


            if (result.status === "success") {

                if (onLogUpdated) {

                    await onLogUpdated();

                }

                onClose();

            } else {

                setErrorMessage(
                    result.message ||
                    "Unable to update log."
                );

            }

        } catch (error) {

            console.error(
                "Failed to update log:",
                error
            );

            setErrorMessage(
                "Unable to update log."
            );

        } finally {

            setIsSaving(false);

        }

    }


    /* =====================================================
       DON'T DISPLAY MODAL WHEN CLOSED
    ===================================================== */

    if (!isOpen || !log) {

        return null;

    }


    return (

        <div className="edit-log-overlay">


            <div className="edit-log-modal">


                {/* =================================================
                   HEADER
                ================================================= */}

                <div className="edit-log-header">

                    <h2>
                        Edit Security Log
                    </h2>


                    <button
                        type="button"
                        className="edit-log-close"
                        onClick={onClose}
                        title="Close"
                        disabled={isSaving}
                    >
                        ×
                    </button>

                </div>


                {/* =================================================
                   BODY
                ================================================= */}

                <div className="edit-log-body">


                    {/* ==============================
                       LOG ID
                    =============================== */}

                    <div className="edit-log-readonly">

                        <span className="edit-log-label">
                            Log ID
                        </span>

                        <span className="edit-log-value">
                            #{log.id}
                        </span>

                    </div>


                    {/* ==============================
                       EVENT
                    =============================== */}

                    <div className="edit-log-readonly-block">

                        <label>
                            Incident / Event
                        </label>

                        <div className="edit-log-static-value">

                            {log.event || "Unknown Event"}

                        </div>

                    </div>


                    {/* ==============================
                       DEVICE
                    =============================== */}

                    <div className="edit-log-readonly-block">

                        <label>
                            Device
                        </label>

                        <div className="edit-log-static-value">

                            {log.device
                                ? (
                                    <>
                                        <strong>
                                            {log.device.hostname}
                                        </strong>

                                        {log.device.ip_address && (
                                            <span className="edit-log-device-ip">
                                                {log.device.ip_address}
                                            </span>
                                        )}
                                    </>
                                )
                                : (
                                    log.device_id
                                        ? `Device #${log.device_id}`
                                        : "Unknown Device"
                                )
                            }

                        </div>

                    </div>


                    {/* ==============================
                       TIMESTAMP
                    =============================== */}

                    <div className="edit-log-readonly-block">

                        <label>
                            Timestamp
                        </label>

                        <div className="edit-log-static-value">

                            {log.timestamp
                                ? new Date(
                                    log.timestamp
                                ).toLocaleString()
                                : "Unknown"}

                        </div>

                    </div>


                    {/* ==============================
                       SEVERITY
                    =============================== */}

                    <div className="edit-log-field">

                        <label>
                            Severity
                        </label>


                        <CustomDropdown

                            options={[
                                "low",
                                "medium",
                                "high"
                            ]}

                            selected={severity}

                            onSelect={setSeverity}

                            fullWidth

                        />

                    </div>


                    {/* ==============================
                       CURRENT STATUS
                    =============================== */}

                    <div className="edit-log-readonly">

                        <span className="edit-log-label">
                            Current Status
                        </span>

                        <span
                            className={`log-status ${log.status}`}
                        >
                            {log.status}
                        </span>

                    </div>


                    {/* ==============================
                       REASON FOR EDIT
                    =============================== */}

                    <div className="edit-log-field">

                        <label>
                            Reason for Edit
                        </label>

                        <textarea
                            value={comment}
                            onChange={(e) =>
                                setComment(e.target.value)
                            }
                            placeholder="Explain why this security log is being edited..."
                            rows="5"
                            disabled={isSaving}
                        />

                        <small className="edit-log-help-text">
                            This reason will be recorded as part of
                            the log modification history.
                        </small>

                    </div>


                    {/* ==============================
                       ERROR
                    =============================== */}

                    {errorMessage && (

                        <div className="edit-log-error">

                            {errorMessage}

                        </div>

                    )}

                </div>


                {/* =================================================
                   FOOTER
                ================================================= */}

                <div className="edit-log-footer">


                    <button
                        type="button"
                        className="edit-log-cancel-btn"
                        onClick={onClose}
                        disabled={isSaving}
                    >
                        Cancel
                    </button>


                    <button
                        type="button"
                        className="edit-log-save-btn"
                        onClick={handleUpdateLog}
                        disabled={isSaving}
                    >

                        {isSaving
                            ? "Saving..."
                            : "Save Changes"}

                    </button>

                </div>


            </div>

        </div>

    );

}


export default EditLogModal;