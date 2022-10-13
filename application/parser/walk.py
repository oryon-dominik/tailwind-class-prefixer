from pathlib import Path
from ..config import settings
from ..inout import read
from .. import exceptions


def parse_file(file: Path):
    """Parse a file for tailwind classes."""
    if not file.is_file():
        raise exceptions.ShallNeverHappen(f"Path {file} is not a file.")
    
    match file.suffix:
        case ".vue":
            from . import vue
            vue.parse(read(file))
        case ".css":
            from . import css
            css.parse(read(file))
        case _:
            raise NotImplementedError(f"File {file} has an not implemented file extension.")


def tree(path: Path) -> None:
    """Walk a directory tree (if not ignored) and parse all files if in allowed extensions."""
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
