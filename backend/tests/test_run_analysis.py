import json
import agent_runner


def test_run_analysis_finds_stale_readme_command(tmp_path):
    package_json = tmp_path / "package.json"
    readme = tmp_path / "README.md"

    package_data = {
        "scripts": {
            "dev": "next dev",
            "build": "next build"
        },
        "dependencies": {},
        "devDependencies": {}
    }

    package_json.write_text(json.dumps(package_data), encoding="utf-8")

    readme.write_text(
        """
        # Test Project

        To run the project:

        npm run dev
        npm run serve
        """,
        encoding="utf-8"
    )

    result = agent_runner.run_maintenance_agent(str(tmp_path))

    assert "repo_map" in result
    assert "package_analysis" in result
    assert "readme_analysis" in result
    assert "findings" in result
    assert "decisions" in result
    assert "selected_context" in result
    assert "suggestion" in result

    assert len(result["findings"]) == 1
    assert result["findings"][0]["type"] == "stale_readme_command"
    assert "serve" in result["findings"][0]["message"]

    assert result["decisions"][0]["action"] == "prioritize_finding"
    assert result["suggestion"]["suggested_action"] == "update_readme_command"