def audit_readme_scripts(package_analysis, readme_analysis):
    findings = []
    
    available_scripts = set()

    for package in package_analysis:
        scripts = package.get("scripts", {})
        available_scripts.update(scripts.keys())

    for readme in readme_analysis:
        readme_commands = readme.get("npm_run_commands", [])

        for command in readme_commands:
            if command not in available_scripts:
                findings.append({
                    "type": "stale_readme_command", 
                    "severity": "medium",
                    "file": readme["path"], 
                    "command": command,
                    "old_text": f"npm run {command}",
                    "message": f"README mentions 'npm run {command}', but package.json does not define a '{command}' script."
                })
                
    return findings