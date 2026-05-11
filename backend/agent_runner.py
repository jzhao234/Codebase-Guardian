import repo_scanner

import analyzers.package_analyzer as package_analyzer
import analyzers.readme_analyzer as readme_analyzer
import analyzers.env_analyzer as env_analyzer
import analyzers.source_env_analyzer as source_env_analyzer

import auditors.resource_auditor as resource_auditor
import auditors.env_auditor as env_auditor


def run_maintenance_agent(repo_path):
    agent_state = {
        "repo_path": repo_path,
        "repo_map": [],
        "package_analysis": [],
        "readme_analysis": [],
        "env_analysis": [],
        "source_env_analysis": [],
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

        if file_info["name"] == ".env.example":
            result = env_analyzer.analyze_env_file(file_info["path"])
            agent_state["env_analysis"].append(result)

        if file_info["category"] == "source_code":
            result = source_env_analyzer.analyze_source_env_usage(file_info["path"])
            agent_state["source_env_analysis"].append(result)

    readme_findings = resource_auditor.audit_readme_scripts(
        agent_state["package_analysis"],
        agent_state["readme_analysis"]
    )

    env_findings = env_auditor.audit_env_example(
        agent_state["env_analysis"],
        agent_state["source_env_analysis"]
    )

    agent_state["findings"].extend(readme_findings)
    agent_state["findings"].extend(env_findings)

    if agent_state["findings"]:
        agent_state["decisions"].append({
            "decision": "report_findings",
            "reason": "The agent found stale or inconsistent project resources.",
            "finding_count": len(agent_state["findings"])
        })
    else:
        agent_state["decisions"].append({
            "decision": "no_action_needed",
            "reason": "No issues were found by the current checks.",
            "finding_count": 0
        })

    return agent_state