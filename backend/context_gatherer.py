def read_file_text(path, max_chars=4000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        return content[:max_chars]

    except OSError as error:
        return f"Could not read file: {error}"


def gather_context_for_finding(finding, agent_state):
    finding_type = finding.get("type")

    if finding_type == "stale_readme_command":
        return {
            "finding_type": finding_type,
            "finding": finding,
            "related_readme_files": [
                {
                    "path": readme["path"],
                    "content_preview": read_file_text(readme["path"])
                }
                for readme in agent_state["readme_analysis"]
            ],
            "related_package_files": agent_state["package_analysis"],
        }

    if finding_type == "missing_env_example_var":
        return {
            "finding_type": finding_type,
            "finding": finding,
            "source_file_preview": read_file_text(finding["file"]),
            "env_example_files": agent_state["env_analysis"],
        }

    return {
        "finding_type": finding_type,
        "finding": finding,
        "context": "No context gatherer implemented for this finding type yet."
    }