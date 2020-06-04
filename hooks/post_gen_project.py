# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
import os
import secrets
import shutil
import string
import subprocess
from typing import Dict, List

DOCS_SOURCES = "docs_sources"

ALL_TEMP_FOLDERS = [DOCS_SOURCES, "licenses"]

DOCS_FILES_BY_TOOL = {
    "mkdocs": [
        "index.md",
        "css",
        "js",
        "reference",
        "/mkdocs.yml"
    ],
}


def get_random_string(
    *,
    length: int = 50,
    allowed_chars: str = f"{string.ascii_letters}{string.digits}",
) -> str:
    """
    Return a securely generated random string.
    """

    return "".join(secrets.choice(allowed_chars) for i in range(length))


def create_git_repo() -> None:
    try:
        subprocess.call(["git", "init", "-q"])
        os.rename("git_ignore", ".gitignore")

    except Exception as error:
        print(error)

def create_env_file() -> None:
    # logger.info(f"Initializing .env")
    env_file = f"""DEBUG=True
SECRET_KEY={get_random_string()}
ALLOWED_HOSTS=["*"]
DATABASE_URL=sqlite://./db.sqlite3
    """
    with open(".env", "w") as file:
        file.write(env_file)


def move_docs_files(
    *, docs_tool: str, docs_files: Dict[str, List[str]], docs_sources: str
) -> None:
    if docs_tool == "none":
        return None

    root = os.getcwd()
    docs = "docs"

    # logger.info(f"Initializing docs for {docs_tool}")
    if not os.path.exists(docs):
        os.mkdir(docs)

    for item in docs_files[docs_tool]:
        dst, name = (root, item[1:]) if item.startswith("/") else (docs, item)
        src_path = os.path.join(docs_sources, docs_tool, name)
        dst_path = os.path.join(dst, name)

        # logger.info(f"Moving {src_path} to {dst_path}.")
        if os.path.exists(dst_path):
            os.unlink(dst_path)

        os.rename(src_path, dst_path)

def remove_temp_folders(*, temp_folders: List[str]) -> None:
    for folder in temp_folders:
        # logger.info(f"Remove temporary folder: {folder}")
        shutil.rmtree(folder)


if __name__ == "__main__":
    move_docs_files(
        docs_tool="{{cookiecutter.docs_tool}}",
        docs_files=DOCS_FILES_BY_TOOL,
        docs_sources=DOCS_SOURCES,
    )
    remove_temp_folders(temp_folders=ALL_TEMP_FOLDERS)
    create_env_file()
    create_git_repo()
