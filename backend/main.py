import json
import argparse

import agent_runner
import repo_loader

def main():
    parser = argparse.ArgumentParser(description="Analyze a codebase for stale resources.")
    parser.add_argument("--repo", required=True, help="Local repo path or GitHub URL")
    parser.add_argument("--output", default="analysis_output.json", help="Output JSON file")

    args = parser.parse_args()

    with repo_loader.prepare_repo(args.repo) as repo_path:
        output = agent_runner.run_maintenance_agent(repo_path)

    with open(args.output, "w") as file:
        json.dump(output, file, indent=4)

    print(f"Analysis saved to {args.output}")

if __name__ == "__main__":
    main()