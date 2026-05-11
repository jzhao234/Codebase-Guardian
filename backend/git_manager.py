import subprocess
import time


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