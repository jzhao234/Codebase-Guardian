import os

def ignore_rules():
    dir_list = {
        "node_modules",
        ".git",
        ".next",
        "venv",
        "__pycache__",
        "dist",
        "build",
    }
    file_list = {
        ".DS_Store",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    }
    extension_list = {
        ".png",
        ".jpg",
        ".gif",
        ".ico",
        ".pyc",
    }
    return dir_list, file_list, extension_list


def scan_repo(path): 
    repo_files = []
    dir_list, file_list, extension_list = ignore_rules()
    for root, dirs, files in os.walk(path, topdown=True):
        for dir_name in dir_list:
            if dir_name in dirs:
                dirs.remove(dir_name)
            
        for file in files:
            if file in file_list or file.endswith(tuple(extension_list)):
                continue
            full_path = os.path.join(root, file)
            repo_files.append(full_path)
    return repo_files