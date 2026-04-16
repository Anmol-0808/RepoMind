import os
from git import Repo


def clone_repo(repo_url: str, base_dir: str = "repos"):

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        print("Repo already exists")
        return repo_path

    print("Cloning repo...")
    Repo.clone_from(repo_url, repo_path)

    return repo_path


def is_code_file(file_path: str):
    extensions = [
        ".py", ".js", ".ts", ".tsx",
        ".java", ".cpp", ".c",
        ".go", ".rs",
        ".html", ".css",
        ".json", ".md", ".yaml", ".yml"
    ]

    return any(file_path.endswith(ext) for ext in extensions)


def load_repository_files(repo_path: str):

    files_data = []

    ignored_dirs = ["node_modules", "venv", "dist", "build", "__pycache__"]
    MAX_FILE_SIZE = 200_000

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]

        for file in files:

            full_path = os.path.join(root, file)

            if not is_code_file(full_path):
                continue

            if os.path.getsize(full_path) > MAX_FILE_SIZE:
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:

                    files_data.append({
                        "path": full_path,
                        "relative_path": os.path.relpath(full_path, repo_path),
                        "file_name": file,
                        "content": f.read()
                    })

            except Exception as e:
                print(f"Error reading {full_path}: {e}")

    return files_data