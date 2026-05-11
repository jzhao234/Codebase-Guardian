import repo_scanner
import context_gatherer
import suggestion_generator
import backend.decision_engine as decision_engine

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
        "selected_context": None,
        "suggestion": None,
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

    ranked_findings = decision_engine.rank_findings(agent_state["findings"])
    agent_state["findings"] = ranked_findings

    next_action = decision_engine.choose_next_action(ranked_findings)
    agent_state["decisions"].append(next_action)

    if next_action["action"] == "prioritize_finding":
        selected_finding = next_action["selected_finding"]

        selected_context = context_gatherer.gather_context_for_finding(
            selected_finding,
            agent_state
        )

        agent_state["selected_context"] = selected_context
    
    suggestion = suggestion_generator.generate_suggestion(selected_context)
    agent_state["suggestion"] = suggestion

    return agent_state