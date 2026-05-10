import json
import argparse

import repo_scanner
import repo_loader
import analyzers.package_analyzer as package_analyzer
import analyzers.readme_analyzer as readme_analyzer
import analyzers.env_analyzer as env_analyzer
import analyzers.source_env_analyzer as source_env_analyzer

import auditors.env_auditor as env_auditor
import auditors.resource_auditor as resource_auditor

def run_analysis(repo_path):
    repo_map = repo_scanner.scan_repo('.')

    findings = []
    package_results = []
    readme_results = []
    env_results = []
    source_env_results = []

    for file_info in repo_map:
        if file_info["name"] == "package.json":
            result = package_analyzer.analyze_package_json(file_info["path"])
            package_results.append(result)
        if file_info["name"].lower() == "readme.md":
            result = readme_analyzer.analyze_readme(file_info["path"])
            readme_results.append(result)
        if file_info["name"] == ".env.example":
            result = env_analyzer.analyze_env_file(file_info["path"])
            env_results.append(result)
        if file_info["category"] == "source_code":
            result = source_env_analyzer.analyze_source_env_usage(file_info["path"])
            source_env_results.append(result)
    
    readme_findings = resource_auditor.audit_readme_scripts(
        package_results,
        readme_results
    )

    env_findings = env_auditor.audit_env_example(
        env_results,
        source_env_results
    )

    findings.extend(readme_findings)
    findings.extend(env_findings)
    
    output = {
        "repo_map": repo_map,
        "package_analysis": package_results,
        "readme_analysis": readme_results,
        "env_analysis": env_results,
        "source_env_analysis": source_env_results,
        "findings": findings,
    }
    
def main():
    parser = argparse.ArgumentParser(description="Analyze a codebase for stale resources.")
    parser.add_argument("--repo", required=True, help="Local repo path or GitHub URL")
    parser.add_argument("--output", default="analysis_output.json", help="Output JSON file")

    args = parser.parse_args()

    with repo_loader.prepare_repo(args.repo) as repo_path:
        output = run_analysis(repo_path)

    with open("analysis_output.json", "w") as file:
        json.dump(output, file, indent=4)

    print("Analysis saved to analysis_output.json")

if __name__ == "__main__":
    main()