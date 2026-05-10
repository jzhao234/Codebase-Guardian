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
                "category": categorize_file(file, extension, full_path)
            }

            repo_files.append(file_info)

    return repo_files

def categorize_file(filename, extension, full_path):
    filename = filename.lower()
    extension = extension.lower()

    if extension == ".md":
        return "documentation"

    if filename in {"package.json", "requirements.txt", "pyproject.toml"}:
        return "dependency"

    if filename in {".env", ".env.example"}:
        return "environment"

    if filename == "dockerfile" or extension in {".yml", ".yaml"}:
        return "config"

    if extension in {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".cpp"}:
        return "source_code"

    return "unknown"