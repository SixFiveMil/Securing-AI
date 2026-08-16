"""
Blue Team Scaffolded Rules (Intermediate Tier)
==============================================
This preset gives students a partial starting point.
Use lowercase strings for consistent case-insensitive matching.
"""

# INGRESS: include phrases to block before model execution.
INGRESS_BLACKLIST = [
    # Example syntax: "ignore all",
    # Example syntax: "system prompt",
    "ignore all",
    "ignore previous",
    # "disregard",
    # "override",
    # "roleplay",
    # "fictional story",
    # "as an administrator",
    # "maintenance technician",
]

# EGRESS: exact secrets are intentionally scaffolded as commented entries.
EGRESS_SECRETS = [
    # "NP-SYS-PROD-01",
    # "NP-ADMIN-9921-X",
    # "db-internal.northpeakcu.local",
    # "/override_admin_mode",
    # "MORTGAGE_VIP_2026",
]

# EGRESS: minimal phrase checks students can expand.
EGRESS_PATTERNS = [
    "admin override token",
]