
from flask import (
    Blueprint,
    jsonify
)

from database.db import get_db_connection

from services.dashboard_service import (
    get_dashboard_stats_service
)

from utils.auth import (
    login_required
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route('/api/v1/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():

    result, status_code = get_dashboard_stats_service()

    return jsonify(result), status_code