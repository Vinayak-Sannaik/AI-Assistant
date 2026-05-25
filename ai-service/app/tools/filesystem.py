from pathlib import Path


def read_file_tool(path: str) -> dict:

    file_path = Path(path)

    if not file_path.exists():

        return {
            "success": False,
            "error": "File does not exist.",
        }

    if not file_path.is_file():

        return {
            "success": False,
            "error": "Path is not a file.",
        }

    try:

        content = file_path.read_text()

        return {
            "success": True,
            "path": str(file_path),
            "content": content,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


def list_files_tool(
    path: str,
) -> dict:

    directory = Path(path)

    if not directory.exists():

        return {
            "success": False,
            "error": "Directory does not exist.",
        }

    if not directory.is_dir():

        return {
            "success": False,
            "error": "Path is not a directory.",
        }

    try:

        files = []

        for item in directory.iterdir():

            files.append(
                {
                    "name": item.name,
                    "type": (
                        "directory"
                        if item.is_dir()
                        else "file"
                    ),
                }
            )

        return {
            "success": True,
            "path": str(directory),
            "files": files,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }