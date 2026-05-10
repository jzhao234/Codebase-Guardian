import os

def get_ignore_rules():
    ignored_dirs = {
        "node_modules",
        ".git",
        ".next",
        "venv",
        "__pycache__",
        "dist",
        "build",
    }
    ignored_files = {
        ".DS_Store",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    }
    ignored_extensions = {
        ".png",
        ".jpg",
        ".gif",
        ".ico",
        ".pyc",
    }
    return ignored_dirs, ignored_files, ignored_extensions


def scan_repo(path): 
    repo_files = []
    ignored_dirs, ignored_files, ignored_extensions = get_ignore_rules()
    
    for root, dirs, files in os.walk(path, topdown=True):
        for dir_name in ignored_dirs:
            if dir_name in dirs:
                dirs.remove(dir_name)
            
        for file in files:

            file_name, extension = os.path.splitext(file)

            if file in ignored_files:
                continue

            if extension in ignored_extensions: 
                continue


            full_path = os.path.join(root, file)

            file_info = {
                "path": full_path,
                "name": file,
                "extension": extension,
                "size": os.path.getsize(full_path),
            }

            repo_files.append(file_info)

    return repo_files