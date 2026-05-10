import repo_scanner

import analyzers.package_analyzer as package_analyzer
import analyzers.readme_analyzer as readme_analyzer

import auditors.resource_auditor as resource_auditor


def run_maintenance_agent(repo_path):
    agent_state = {
        "repo_path": repo_path,
        "repo_map": [],
        "package_analysis": [],
        "readme_analysis": [],
        "findings": [],
        "decisions": [],
    }

    repo_map = repo_scanner.scan_repo(repo_path)
    agent_state["repo_map"] = repo_map

    for file_info in repo_map:
        if file_info["name"] == "package.json":
            result = package_analyzer.analyze_package_json(file_info["path"])
            agent_state["package_analysis"].append(result)

        if file_info["name"].lower() == "readme.md":
            result = readme_analyzer.analyze_readme(file_info["path"])
            agent_state["readme_analysis"].append(result)

    readme_findings = resource_auditor.audit_readme_scripts(
        agent_state["package_analysis"],
        agent_state["readme_analysis"]
    )

    agent_state["findings"].extend(readme_findings)

    if agent_state["findings"]:
        agent_state["decisions"].append({
            "decision": "report_findings",
            "reason": "The agent found stale or inconsistent project resources."
        })
    else:
        agent_state["decisions"].append({
            "decision": "no_action_needed",
            "reason": "No stale resource issues were found by the current checks."
        })

    return agent_state