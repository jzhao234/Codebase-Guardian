import json

import repo_scanner as repo_scanner

def main():
    repo_map = repo_scanner.scan_repo('.')

    with open("repo_map.json", "w") as file:
        json.dump(repo_map, file, indent=4)

    for file in repo_map:
        print(file)

    print("Repo map saved to repo_map.json")

if __name__ == "__main__":
    main()