from typing import Tuple

# Real queue labels from the Tobi-Bueck/customer-support-tickets dataset
QUEUE_KEYWORDS = {
    "Technical Support": [
        "technical", "error", "bug", "crash", "not working", "driver", "firmware",
        "connectivity", "network", "hardware", "software", "device", "printer",
        "wifi", "vpn", "server", "system failure", "outage", "configuration"
    ],
    "Billing and Payments": [
        "billing", "invoice", "payment", "charge", "refund", "subscription",
        "credit card", "overcharge", "discrepancy", "receipt", "due", "fee", "late"
    ],
    "Service Outages and Maintenance": [
        "outage", "maintenance", "downtime", "scheduled", "service disruption",
        "unavailable", "offline", "restore", "interruption", "edd", "disruption"
    ],
    "IT Support": [
        "it support", "cloud", "saas", "infrastructure", "kubernetes", "pipeline",
        "deployment", "server room", "overheating", "access control", "vpn"
    ],
    "Human Resources": [
        "human resources", "hr", "employee", "staff", "payroll", "benefits",
        "office applications", "microsoft office", "license"
    ],
    "Returns and Exchanges": [
        "return", "exchange", "replacement", "refund", "rma", "warranty",
        "defective", "broken item", "swap"
    ],
    "Sales and Pre-Sales": [
        "pricing", "quote", "purchase", "buy", "sales", "pre-sales", "trial",
        "demo", "discount", "proposal", "offer", "license cost"
    ],
    "Product Support": [
        "product", "feature", "specification", "documentation", "manual",
        "integration", "api", "compatibility", "setup", "install"
    ],
    "Customer Service": [
        "feedback", "complaint", "general inquiry", "inquiry", "question",
        "information", "suggestion", "account", "profile"
    ],
    "General Inquiry": [
        "general", "info", "curious", "policy", "procedure", "how to", "guidance"
    ]
}

# Type classification
TYPE_KEYWORDS = {
    "Incident": [
        "urgent", "emergency", "failure", "failed", "down", "crash", "cannot access",
        "disruption", "outage", "blocked", "not responding", "data loss"
    ],
    "Problem": [
        "problem", "issue", "incorrect", "broken", "intermittent", "error", "bug",
        "slow", "unexpected", "not working", "discrepancy"
    ],
    "Change": [
        "change", "update", "upgrade", "modify", "configure", "refactor",
        "revise", "implement", "deploy", "migrate"
    ],
    "Request": [
        "request", "inquiry", "information", "how to", "provide", "details",
        "documentation", "feature request", "query", "question"
    ]
}

# Priority detection from subject+body
PRIORITY_KEYWORDS = {
    "high": [
        "urgent", "emergency", "asap", "critical", "immediately", "severe",
        "not working", "complete failure", "system down", "data breach", "hacked",
        "healthcare", "outage", "cannot operate", "halt", "blocked"
    ],
    "medium": [
        "issue", "problem", "help", "error", "broken", "slow", "intermittent",
        "connectivity", "access", "disrupted"
    ],
    "low": [
        "inquiry", "request", "feedback", "information", "question", "how to",
        "suggestion", "general", "details", "curious"
    ]
}


def analyze_ticket(subject: str, body: str) -> Tuple[str, str, str]:
    """
    Returns (queue, ticket_type, priority) aligned with the HF dataset labels.
    """
    combined = f"{subject} {body}".lower()

    # Determine Queue
    queue = "General Inquiry"
    best_queue_score = 0
    for q, keywords in QUEUE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_queue_score:
            best_queue_score = score
            queue = q

    # Determine Type
    ticket_type = "Request"
    best_type_score = 0
    for t, keywords in TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_type_score:
            best_type_score = score
            ticket_type = t

    # Determine Priority
    priority = "low"
    if any(kw in combined for kw in PRIORITY_KEYWORDS["high"]):
        priority = "high"
    elif any(kw in combined for kw in PRIORITY_KEYWORDS["medium"]):
        priority = "medium"

    return queue, ticket_type, priority
