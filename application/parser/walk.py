import logging

from pathlib import Path

from ..config import settings
from ..inout import read, write
from .. import exceptions

from .prefix import validate, Prefix


log = logging.getLogger("application")


def parse_file(file: Path, prefix: Prefix) -> None:
    """Parse a file for tailwind classes."""
    if not file.is_file():
        raise exceptions.ShallNeverHappen(f"Path {file} is not a file.")

    match file.suffix:
        case ".vue":
            from . import vue
            content: str = vue.parse(bytes=read(file), prefix=prefix)
            write(path=file, bytes=content.encode("utf-8"))
        case ".css":
            from . import css
            content: str = css.parse(bytes=read(file), prefix=prefix)
            write(path=file, bytes=content.encode("utf-8"))
        case ".js":
            from . import js
            content: str = js.parse(bytes=read(file), prefix=prefix)
            write(path=file, bytes=content.encode("utf-8"))
        case _:
            raise NotImplementedError(f"File {file} has an not implemented file extension.")


def search(path: Path, prefix: str, old_prefix="", remove=False) -> None:
    """Search for tailwind config and parse all files."""
    # find the tailwind-config, update to new prefix and save the old prefix first
    prefix = validate(prefix=prefix, remove=remove)
    for _path in path.glob("**/tailwind.config.js"):
        from . import tailwind
        old_prefix = tailwind.parse(path=_path, prefix=prefix)
        break  # only the first (root) config file is allowed
    # walk the tree, replace the old prefix with the new one or add the prefix
    tree(path=path, prefix=Prefix(old=old_prefix, new=prefix))


def tree(path: Path, prefix: Prefix) -> None:
    """Walk a directory tree (if not ignored) and parse all files if in allowed extensions."""
    if path.is_dir() and path.name in settings.IGNORE_DIRECTORIES:
        # skip
        pass
    elif path.is_file() and path.suffix not in settings.ALLOWED_FILE_EXTENSIONS:
        # skip
        pass
    elif path.is_file() and path.suffix in settings.ALLOWED_FILE_EXTENSIONS:
        parse_file(file=path, prefix=prefix)
    elif path.is_dir() and path.name not in settings.IGNORE_DIRECTORIES:
        for child in path.iterdir():
            tree(path=child, prefix=prefix)
    else:
        raise exceptions.ShallNeverHappen(f"Path {path} is neither a file nor a directory.")

