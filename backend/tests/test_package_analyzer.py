import json
import analyzers.package_analyzer as package_analyzer


def test_analyze_package_json_extracts_scripts_and_dependencies(tmp_path):
    package_file = tmp_path / "package.json"

    package_data = {
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start"
        },
        "dependencies": {
            "react": "^19.0.0",
            "next": "^15.0.0"
        },
        "devDependencies": {
            "eslint": "^9.0.0",
            "pytest": "^1.0.0"
        }
    }

    package_file.write_text(json.dumps(package_data), encoding="utf-8")

    result = package_analyzer.analyze_package_json(str(package_file))

    assert result["path"] == str(package_file)

    assert result["scripts"]["dev"] == "next dev"
    assert result["scripts"]["build"] == "next build"
    assert result["scripts"]["start"] == "next start"

    assert "react" in result["dependencies"]
    assert "next" in result["dependencies"]

    assert "eslint" in result["dev_dependencies"]
    assert "pytest" in result["dev_dependencies"]