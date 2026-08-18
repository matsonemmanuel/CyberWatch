from flask import (
    Blueprint,
    jsonify,
    request
)

from services.alert_services import (
    get_alerts_service,
    get_alert_service,
    create_alert_service,
    update_alert_status_service
)

from utils.auth import login_required


# =====================================================
# ALERT BLUEPRINT
# =====================================================

alert_bp = Blueprint(
    "alerts",
    __name__
)


# =====================================================
# GET ALL ALERTS
# =====================================================

@alert_bp.route(
    "/api/v1/alerts",
    methods=["GET"]
)
@login_required
def get_alerts():

    severity = request.args.get("severity")
    status = request.args.get("status")

    result, status_code = get_alerts_service(
        severity,
        status
    )

    return jsonify(result), status_code


# =====================================================
# GET SINGLE ALERT
# =====================================================

@alert_bp.route(
    "/api/v1/alerts/<int:alert_id>",
    methods=["GET"]
)
@login_required
def get_single_alert(alert_id):

    result, status_code = get_alert_service(
        alert_id
    )

    return jsonify(result), status_code


# =====================================================
# CREATE ALERT
# =====================================================

@alert_bp.route(
    "/api/v1/alerts",
    methods=["POST"]
)
@login_required
def create_alert():

    data = request.get_json()

    result, status_code = create_alert_service(
        data
    )

    return jsonify(result), status_code


# =====================================================
# UPDATE ALERT STATUS
# =====================================================

@alert_bp.route(
    "/api/v1/alerts/<int:alert_id>/status",
    methods=["PATCH"]
)
@login_required
def update_alert_status(alert_id):

    data = request.get_json()

    result, status_code = update_alert_status_service(
        alert_id,
        data
    )

    return jsonify(result), status_code