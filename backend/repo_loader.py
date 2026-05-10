import os
import subprocess
import tempfile
from contextlib import contextmanager

def is_github_url(repo_input):
    return repo_input.startswith("https://github.com/") or repo_input.startswith("git@github.com:")


@contextmanager
def prepare_repo(repo_input):
    if os.path.exists(repo_input):
        yield repo_input
        return

    if is_github_url(repo_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_input, temp_dir],
                check=True
            )
            yield temp_dir
        return

    raise ValueError(f"Repo input is not a valid local path or GitHub URL: {repo_input}")