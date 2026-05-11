import json
import argparse

import repo_loader
from agent_core.agent_loop import run_agent_loop


def main():
    parser = argparse.ArgumentParser(description="Analyze a codebase for stale resources.")
    parser.add_argument("--repo", required=True, help="Local repo path or GitHub URL")
    parser.add_argument("--output", default="analysis_output.json", help="Output JSON file")
    parser.add_argument(
        "--apply-fix",
        action="store_true",
        help="Apply the suggested fix locally"
    )

    args = parser.parse_args()

    with repo_loader.prepare_repo(args.repo) as repo_path:
        output = run_agent_loop(
            repo_path,
            apply_fix=args.apply_fix
        )

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    print(f"Analysis saved to {args.output}")


if __name__ == "__main__":
    main()