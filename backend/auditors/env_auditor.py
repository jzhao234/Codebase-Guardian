def audit_env_example(env_analysis, source_env_analysis):
    findings = []

    defined_env_vars = set()

    for env_file in env_analysis:
        defined_env_vars.update(env_file.get("defined_env_vars", []))

    for source_file in source_env_analysis:
        used_env_vars = source_file.get("used_env_vars", [])

        for var_name in used_env_vars:
            if var_name not in defined_env_vars:
                findings.append({
                    "type": "missing_env_example_var",
                    "severity": "high",
                    "file": source_file["path"],
                    "message": f"Source code uses '{var_name}', but it is missing from .env.example."
                })

    return findings