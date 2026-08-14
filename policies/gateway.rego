package gateway

import rego.v1

# -------------------------------------------------------------------
# OPA Policy Template for Phase 3 (Context-Aware Hardening)
# -------------------------------------------------------------------
# Student goals:
# 1) Understand which inputs are considered in-scope vs out-of-scope.
# 2) Tune confidence thresholds to balance usability vs strict security.
# 3) Add/edit ingress and egress controls without changing gateway code.
#
# Keep this file focused on decision logic.
# Edit policy values in policies/rules.json for most exercises.

# Default outcome: allow. Specific rules below override this using
# ordered else branches.
default decision := {
  "allow": true,
  "action": "allow",
  "reason": "no policy match",
  "matched": []
}

# A valid classifier context should include both domain and intent.
has_context if {
  input.context.domain
  input.context.intent
}

# Domain allowed list from rules.json (student-editable data).
domain_allowed if {
  some i
  data.policy.allowed_domains[i] == input.context.domain
}

# Intents that must always be blocked.
intent_blocked if {
  some i
  data.policy.blocked_intents[i] == input.context.intent
}

# Domain-to-intent mapping for in-scope requests.
intent_allowed_for_domain if {
  intents := object.get(data.policy.allowed_intents, input.context.domain, [])
  some i
  intents[i] == input.context.intent
}

# ----------------------------
# Derived match collections
# ----------------------------
# Each collection returns all matched values for explainable logging.

ingress_matches := [
  phrase |
  input.stage == "ingress"
  phrase := data.policy.ingress_blacklist[_]
  contains(lower(input.prompt), lower(phrase))
]

egress_secret_matches := [
  secret |
  input.stage == "egress"
  secret := data.policy.egress_secrets[_]
  contains(lower(input.response), lower(secret))
]

egress_pattern_matches := [
  pattern |
  input.stage == "egress"
  pattern := data.policy.egress_patterns[_]
  contains(lower(input.response), lower(pattern))
]

high_risk_matches := [
  flag |
  has_context
  flag := input.context.risk_flags[_]
  lower(flag) == lower(data.policy.high_risk_flags[_])
]

# ----------------------------
# Context reason builders
# ----------------------------
# Ordered reason chain. First match wins.

context_block_reason := reason if {
  has_context
  not domain_allowed
  reason := sprintf("context domain '%s' is out of scope", [input.context.domain])
} else := reason if {
  has_context
  intent_blocked
  reason := sprintf("context intent '%s' is blocked", [input.context.intent])
} else := reason if {
  has_context
  not intent_allowed_for_domain
  reason := sprintf("intent '%s' is not allowed for domain '%s'", [input.context.intent, input.context.domain])
} else := reason if {
  has_context
  input.context.confidence < data.policy.confidence_threshold_clarify
  reason := sprintf("classifier confidence %.2f below block threshold %.2f", [input.context.confidence, data.policy.confidence_threshold_clarify])
}

# Clarification band: classifier is not trusted enough to allow,
# but not low-confidence enough to hard-block.
context_clarify_reason := reason if {
  has_context
  input.context.confidence >= data.policy.confidence_threshold_clarify
  input.context.confidence < data.policy.confidence_threshold_allow
  reason := sprintf("classifier confidence %.2f requires clarification", [input.context.confidence])
}

# ----------------------------
# Final decision chain
# ----------------------------
# This chain is intentionally ordered.
# Priority:
# 1) Ingress hard matches
# 2) Ingress high-risk context
# 3) Ingress context policy violations
# 4) Ingress clarification
# 5) Egress secret/pattern leaks
# 6) Default allow

decision := {
  "allow": false,
  "action": "block_ingress",
  "reason": "ingress blacklist match",
  "matched": ingress_matches
} if {
  input.stage == "ingress"
  count(ingress_matches) > 0
} else := {
  "allow": false,
  "action": "block_ingress",
  "reason": "classifier flagged high risk",
  "matched": high_risk_matches
} if {
  input.stage == "ingress"
  count(high_risk_matches) > 0
} else := {
  "allow": false,
  "action": "block_ingress",
  "reason": context_block_reason,
  "matched": ["context_policy"]
} if {
  input.stage == "ingress"
  context_block_reason
} else := {
  "allow": false,
  "action": "require_clarification",
  "reason": context_clarify_reason,
  "matched": ["context_threshold"]
} if {
  input.stage == "ingress"
  context_clarify_reason
} else := {
  "allow": false,
  "action": "block_egress",
  "reason": "egress secret match",
  "matched": egress_secret_matches
} if {
  input.stage == "egress"
  count(egress_secret_matches) > 0
} else := {
  "allow": false,
  "action": "block_egress",
  "reason": "egress pattern match",
  "matched": egress_pattern_matches
} if {
  input.stage == "egress"
  count(egress_pattern_matches) > 0
}
