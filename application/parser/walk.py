from pathlib import Path
import logging

from ..config import settings
from ..inout import read, write
from .. import exceptions


log = logging.getLogger("application")


def parse_file(file: Path, new_prefix: str, old_prefix: str) -> None:
    """Parse a file for tailwind classes."""
    if not file.is_file():
        raise exceptions.ShallNeverHappen(f"Path {file} is not a file.")

    match file.suffix:
        case ".vue":
            from . import vue
            content: str = vue.parse(bytes=read(file), new_prefix=new_prefix, old_prefix=old_prefix)
            write(path=file, bytes=content.encode("utf-8"))
        case ".css":
            from . import css
            css.parse(bytes=read(file), new_prefix=new_prefix, old_prefix=old_prefix)
        case _:
            raise NotImplementedError(f"File {file} has an not implemented file extension.")


def search(path: Path, prefix: str, old_prefix="") -> None:
    """Search for tailwind config and parse all files."""
    # find the tailwind-config, update to new prefix and save the old prefix first
    for _path in path.glob("**/tailwind.config.js"):
        from . import tailwind
        old_prefix = tailwind.parse(path=_path, prefix=prefix)
        break  # only the first (root) config file is allowed
    # walk the tree, replace the old prefix with the new one or add the prefix
    tree(path=path, new_prefix=prefix, old_prefix=old_prefix)


def tree(path: Path, new_prefix: str, old_prefix: str) -> None:
    """Walk a directory tree (if not ignored) and parse all files if in allowed extensions."""
    if path.is_dir() and path.name in settings.IGNORE_DIRECTORIES:
        # skip
        pass
    elif path.is_file() and path.suffix not in settings.ALLOWED_FILE_EXTENSIONS:
        # skip
        pass
    elif path.is_file() and path.suffix in settings.ALLOWED_FILE_EXTENSIONS:
        parse_file(file=path, new_prefix=new_prefix, old_prefix=old_prefix)
    elif path.is_dir() and path.name not in settings.IGNORE_DIRECTORIES:
        for child in path.iterdir():
            tree(path=child, new_prefix=new_prefix, old_prefix=old_prefix)
    else:
        raise exceptions.ShallNeverHappen(f"Path {path} is neither a file nor a directory.")

