def is_same_finding(original_finding, remaining_finding):
    if original_finding.get("type") != remaining_finding.get("type"):
        return False

    if original_finding.get("file") != remaining_finding.get("file"):
        return False

    if "command" in original_finding:
        return original_finding.get("command") == remaining_finding.get("command")

    return original_finding.get("message") == remaining_finding.get("message")


def verify_fix(repo_path, selected_finding, run_analysis_pass):
    verification_state = run_analysis_pass(repo_path)
    remaining_findings = verification_state["findings"]

    selected_finding_still_present = any(
        is_same_finding(selected_finding, finding)
        for finding in remaining_findings
    )

    return {
        "reran_analysis": True,
        "selected_finding_resolved": not selected_finding_still_present,
        "remaining_findings_count": len(remaining_findings),
        "remaining_findings": remaining_findings,
    }