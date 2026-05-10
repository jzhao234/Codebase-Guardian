import re

def analyze_readme(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

        npm_commands = re.findall(r"npm run ([a-zA-Z0-9:_=]+)", content)

        return {
            "path": path, 
            "npm_run_commands": npm_commands,
        }