import os
import subprocess
from contextlib import contextmanager


def is_github_url(repo_input):
    return repo_input.startswith("https://github.com/") or repo_input.startswith("git@github.com:")


def get_repo_name(repo_url):
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    return repo_name


@contextmanager
def prepare_repo(repo_input, workspace_dir=".workspaces"):
    if os.path.exists(repo_input):
        yield repo_input
        return

    if is_github_url(repo_input):
        os.makedirs(workspace_dir, exist_ok=True)

        repo_name = get_repo_name(repo_input)
        local_repo_path = os.path.join(workspace_dir, repo_name)

        if not os.path.exists(local_repo_path):
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_input, local_repo_path],
                check=True
            )
        else:
            subprocess.run(
                ["git", "-C", local_repo_path, "pull"],
                check=True
            )

        yield local_repo_path
        return

    raise ValueError(f"Repo input is not a valid local path or GitHub URL: {repo_input}")