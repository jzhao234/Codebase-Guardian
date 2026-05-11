def severity_score(severity):
    scores = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
        "info": 0,
    }

    return scores.get(severity, 0)


def rank_findings(findings):
    return sorted(
        findings,
        key=lambda finding: severity_score(finding.get("severity", "info")),
        reverse=True
    )


def choose_next_action(findings):
    if not findings:
        return {
            "action": "no_action_needed",
            "reason": "No findings were detected."
        }

    ranked_findings = rank_findings(findings)
    top_finding = ranked_findings[0]

    return {
        "action": "prioritize_finding",
        "reason": "The agent selected the highest-severity finding to address first.",
        "selected_finding": top_finding
    }