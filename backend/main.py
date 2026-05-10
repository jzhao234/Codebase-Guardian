import json

import repo_scanner as repo_scanner
import analyzers.package_analyzer as package_analyzer

def main():
    repo_map = repo_scanner.scan_repo('.')

    package_results = []

    for file_info in repo_map:
        if file_info["name"] == "package.json":
            result = package_analyzer.analyze_package_json(file_info["path"])
            package_results.append(result)
    
    output = {
        "repo_map": repo_map,
        "package_analysis": package_results
    }

    with open("analysis_output.json", "w") as file:
        json.dump(output, file, indent=4)

    print("Analysis saved to analysis_output.json")

if __name__ == "__main__":
    main()