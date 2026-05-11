import auditors.resource_auditor as resource_auditor

def test_audit_readme_scripts_finds_missing_script():
    package_analysis = [
        {
            "scripts": {
                "dev": "next dev",
                "build": "next build"
            }
        }
    ]

    readme_analysis = [
        {
            "path": "README.md",
            "npm_run_commands": ["dev", "serve"]
        }
    ]

    findings = resource_auditor.audit_readme_scripts(
        package_analysis,
        readme_analysis
    )

    assert len(findings) == 1
    assert findings[0]["type"] == "stale_readme_command"
    assert "serve" in findings[0]["message"]