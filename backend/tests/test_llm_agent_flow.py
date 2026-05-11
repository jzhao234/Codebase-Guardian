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


def create_demo_repo(tmp_path):
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

    return readme


def test_agent_uses_mocked_llm_suggestion_without_applying_fix(tmp_path, monkeypatch):
    create_demo_repo(tmp_path)

    def fake_llm_suggestion(selected_context):
        finding = selected_context["finding"]

        return {
            "used_llm": True,
            "suggested_action": "update_readme_command",
            "confidence": "high",
            "finding": finding,
            "file_to_edit": finding["file"],
            "old_text": "npm run serve",
            "new_text": "npm run dev",
            "suggested_fix": "Replace 'npm run serve' with 'npm run dev'.",
            "reason": "The README describes local development, and package.json defines a dev script."
        }

    monkeypatch.setattr(
        "agent_core.agent_tools.generate_llm_suggestion",
        fake_llm_suggestion
    )

    result = run_agent_loop(
        str(tmp_path),
        apply_fix=False,
        use_llm=True
    )

    assert result["suggestion"]["used_llm"] is True
    assert result["suggestion"]["suggested_action"] == "update_readme_command"
    assert result["suggestion"]["new_text"] == "npm run dev"

    assert result["fix_result"] is None or result["fix_result"]["applied"] is False
    assert result["final_status"] == "A suggestion was generated, but apply_fix is disabled."


def test_agent_applies_mocked_llm_suggestion_and_verifies(tmp_path, monkeypatch):
    readme = create_demo_repo(tmp_path)

    setup_git_repo(tmp_path)
    commit_initial_state(tmp_path)

    def fake_llm_suggestion(selected_context):
        finding = selected_context["finding"]

        return {
            "used_llm": True,
            "suggested_action": "update_readme_command",
            "confidence": "high",
            "finding": finding,
            "file_to_edit": finding["file"],
            "old_text": "npm run serve",
            "new_text": "npm run dev",
            "suggested_fix": "Replace 'npm run serve' with 'npm run dev'.",
            "reason": "The README describes local development, and package.json defines a dev script."
        }

    monkeypatch.setattr(
        "agent_core.agent_tools.generate_llm_suggestion",
        fake_llm_suggestion
    )

    result = run_agent_loop(
        str(tmp_path),
        apply_fix=True,
        use_llm=True
    )

    updated_readme = readme.read_text(encoding="utf-8")

    assert "npm run serve" not in updated_readme
    assert "npm run dev" in updated_readme

    assert result["suggestion"]["used_llm"] is True
    assert result["fix_result"]["applied"] is True

    assert result["verification"]["reran_analysis"] is True
    assert result["verification"]["selected_finding_resolved"] is True

    assert result["commit"]["success"] is True
    assert result["commit"]["committed"] is True

    assert result["diff"]["success"] is True
    assert "npm run serve" in result["diff"]["diff"]
    assert "npm run dev" in result["diff"]["diff"]