import re

def analyze_source_env_usage(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    patterns = [
        r"process\.env\.([A-Za-z_][A-Za-z0-9_]*)",
        r"os\.environ\[['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\]",
        r"os\.getenv\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]",
    ]

    used_env_vars = set()

    for pattern in patterns:
        matches = re.findall(pattern, content)
        used_env_vars.update(matches)

    return {
        "path": path,
        "used_env_vars": sorted(used_env_vars),
    }