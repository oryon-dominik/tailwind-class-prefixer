from pathlib import Path
from ..config import settings
from .. import exceptions

def parse_file(file: Path):
    """Parse a file for tailwind classes."""
    if not file.is_file():
        raise exceptions.ShallNeverHappen(f"Path {file} is not a file.")

    print(file.name)
    # with open(file_path, "r") as f:
    #     content = f.read()
    #     for line in content.splitlines():
    #         if line.startswith(settings.TAILWIND_DEFAULT_PREFIX):
    #             print(line)


def tree(path: Path) -> None:
    """Print a directory tree."""
    if path.is_dir() and path.name in settings.IGNORE_DIRECTORIES:
        # skip
        pass
    elif path.is_file() and path.suffix not in settings.ALLOWED_FILE_EXTENSIONS:
        # skip
        pass
    elif path.is_file() and path.suffix in settings.ALLOWED_FILE_EXTENSIONS:
        parse_file(file=path)
    elif path.is_dir() and path.name not in settings.IGNORE_DIRECTORIES:
        for child in path.iterdir():
            tree(path=child)
    else:
        raise exceptions.ShallNeverHappen(f"Path {path} is neither a file nor a directory.")
