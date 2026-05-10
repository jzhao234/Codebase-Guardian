def analyze_env_file(path):
    env_vars = []

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            var_name = line.split("=", 1)[0].strip()

            if var_name:
                env_vars.append(var_name)

    return {
        "path": path,
        "defined_env_vars": env_vars,
    }