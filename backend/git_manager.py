import subprocess
import time

def has_changes(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "status", "--porcelain"],
        capture_output=True,
        text=True
    )

    return bool(result.stdout.strip())


def commit_changes(repo_path, message):
    if not has_changes(repo_path):
        return {
            "success": False,
            "committed": False,
            "error": "No changes to commit."
        }

    add_result = subprocess.run(
        ["git", "-C", repo_path, "add", "."],
        capture_output=True,
        text=True
    )

    if add_result.returncode != 0:
        return {
            "success": False,
            "committed": False,
            "error": add_result.stderr
        }

    commit_result = subprocess.run(
        ["git", "-C", repo_path, "commit", "-m", message],
        capture_output=True,
        text=True
    )

    if commit_result.returncode != 0:
        return {
            "success": False,
            "committed": False,
            "error": commit_result.stderr
        }

    return {
        "success": True,
        "committed": True,
        "message": message,
        "error": None
    }

def create_fix_branch(repo_path, prefix="agent-fix"):
    branch_name = f"{prefix}-{int(time.time())}"

    result = subprocess.run(
        ["git", "-C", repo_path, "checkout", "-b", branch_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "success": False,
            "branch": None,
            "error": result.stderr
        }

    return {
        "success": True,
        "branch": branch_name,
        "error": None
    }