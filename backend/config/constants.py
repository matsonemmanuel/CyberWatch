
"""
CyberWatch System Constants

This module contains reusable constant values shared across
the application to improve consistency and maintainability.
"""


# User Roles
ALLOWED_USER_ROLES = (
    "admin",
    "analyst"
)

# Log Severity Levels
ALLOWED_LOG_SEVERITIES = (
    "low",
    "medium",
    "high"
)

# Incident Statuses
ALLOWED_LOG_STATUSES = (
    "open",
    "investigating",
    "resolved"
)

# Device Statuses
ALLOWED_DEVICE_STATUSES = (
    "active",
    "disabled",
    "offline"
)