import json

import repo_scanner as repo_scanner
import analyzers.package_analyzer as package_analyzer
import analyzers.readme_analyzer as readme_analyzer

import auditors.resource_auditor as resource_auditor

def main():
    repo_map = repo_scanner.scan_repo('.')

    package_results = []
    readme_results = []

    for file_info in repo_map:
        if file_info["name"] == "package.json":
            result = package_analyzer.analyze_package_json(file_info["path"])
            package_results.append(result)
        if file_info["name"].lower() == "readme.md":
            result = readme_analyzer.analyze_readme(file_info["path"])
            readme_results.append(result)
    
    findings = resource_auditor.audit_readme_scripts(
        package_results,
        readme_results
    )
    
    output = {
        "repo_map": repo_map,
        "package_analysis": package_results,
        "readme_analysis": readme_results,
        "findings": findings,
    }

    with open("analysis_output.json", "w") as file:
        json.dump(output, file, indent=4)

    print("Analysis saved to analysis_output.json")

if __name__ == "__main__":
    main()