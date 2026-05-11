import json
import subprocess

from agent_core.agent_loop import run_agent_loop

def setup_git_repo(repo_path):
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)


def commit_initial_state(repo_path):
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)


def test_agent_applies_readme_fix_and_verifies(tmp_path):
    package_json = tmp_path / "package.json"
    readme = tmp_path / "README.md"

    package_json.write_text(
        json.dumps({
            "scripts": {
                "dev": "next dev",
                "build": "next build"
            },
            "dependencies": {},
            "devDependencies": {}
        }),
        encoding="utf-8"
    )

    readme.write_text(
        """
        # Test Project

        To run this project:

        npm run serve
        """,
        encoding="utf-8"
    )

    setup_git_repo(tmp_path)
    commit_initial_state(tmp_path)

    result = run_agent_loop(
        str(tmp_path),
        apply_fix=True
    )

    updated_readme = readme.read_text(encoding="utf-8")

    assert "npm run serve" not in updated_readme
    assert "npm run dev" in updated_readme

    assert result["branch"]["success"] is True
    assert result["fix_result"]["applied"] is True

    assert result["suggestion"]["suggested_action"] == "update_readme_command"
    assert result["suggestion"]["old_text"] == "npm run serve"
    assert result["suggestion"]["new_text"] == "npm run dev"

    assert result["diff"]["success"] is True
    assert "npm run serve" in result["diff"]["diff"]
    assert "npm run dev" in result["diff"]["diff"]

    assert result["verification"]["reran_analysis"] is True
    assert result["verification"]["remaining_findings_count"] == 0

    assert result["commit"]["success"] is True
    assert result["commit"]["committed"] is True