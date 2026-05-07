import repo_scanner as repo_scanner

def main():
    repo_files = repo_scanner.scan_repo('.')
    for file in repo_files:
        print(file)

if __name__ == "__main__":
    main()