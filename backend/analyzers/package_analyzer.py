import json

def analyze_package_json(path):
    with open(path, "r") as file:
        data = json.load(file)

    scripts = data.get("scripts", {})
    dependencies = data.get("dependencies", {})
    dev_dependencies = data.get("devDependencies", {})

    return {
        "path": path, 
        "scripts": scripts,
        "dependencies": list(dependencies.keys()),
        "dev_dependencies": list(dev_dependencies.keys()),
    }