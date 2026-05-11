import subprocess


def generate_git_diff(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "diff"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "success": False,
            "diff": "",
            "error": result.stderr
        }

    return {
        "success": True,
        "diff": result.stdout,
        "error": None
    }