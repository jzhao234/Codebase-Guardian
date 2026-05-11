def generate_suggestion(selected_context):
    if selected_context is None:
        return None

    finding = selected_context.get("finding", {})
    finding_type = selected_context.get("finding_type")

    if finding_type == "stale_readme_command":
        return suggest_readme_command_fix(selected_context)

    if finding_type == "missing_env_example_var":
        return suggest_env_example_fix(selected_context)

    return {
        "suggested_action": "manual_review",
        "confidence": "low",
        "reason": "No suggestion generator exists for this finding type yet.",
        "finding": finding,
    }


def suggest_readme_command_fix(selected_context):
    finding = selected_context["finding"]

    package_files = selected_context.get("related_package_files", [])

    available_scripts = set()

    for package in package_files:
        scripts = package.get("scripts", {})
        available_scripts.update(scripts.keys())

    suggested_replacement = None

    if "dev" in available_scripts:
        suggested_replacement = "npm run dev"
    elif "start" in available_scripts:
        suggested_replacement = "npm run start"
    elif available_scripts:
        first_script = sorted(available_scripts)[0]
        suggested_replacement = f"npm run {first_script}"

    if suggested_replacement:
        return {
            "suggested_action": "update_readme_command",
            "confidence": "medium",
            "finding": finding,
            "file_to_edit": finding["file"],
            "old_text": finding["old_text"],
            "new_text": suggested_replacement,
            "suggested_fix": f"Replace '{finding['old_text']}' with '{suggested_replacement}'.",
            "reason": "The README references an npm script that does not exist in package.json, but package.json contains a likely replacement script.",
            "available_scripts": sorted(available_scripts),
        }

    return {
        "suggested_action": "manual_review",
        "confidence": "low",
        "finding": finding,
        "suggested_fix": "Review the README command manually.",
        "reason": "No package.json scripts were available to suggest a replacement.",
        "available_scripts": [],
    }


def suggest_env_example_fix(selected_context):
    finding = selected_context["finding"]

    message = finding.get("message", "")

    return {
        "suggested_action": "update_env_example",
        "confidence": "medium",
        "finding": finding,
        "suggested_fix": "Add the missing environment variable to .env.example with an empty placeholder value.",
        "reason": message,
    }