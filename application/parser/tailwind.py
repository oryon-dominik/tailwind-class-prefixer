import logging
import io
import re
from pathlib import Path

from parse import findall

from ..config import settings
from ..inout import read, write, json
from .. import exceptions


log = logging.getLogger("application")


def get_tailwind_classes_list() -> list:
    """Get a list of all tailwind classes."""
    return json.load_json_from_file(path=settings.TAILWIND_CLASSES_JSON_PATH)


def get_semicolon_style(content: str) -> str:
    """parse semicolon styles, because JavaScript is inconsistent -.-"""
    semicolon_style_double = '"' in content
    semicolon_style_single = "'" in content
    if semicolon_style_double and semicolon_style_single:
        raise exceptions.ShallNeverHappen("Cannot parse file, both single and double quotes are used. Invalid tailwind.config.js")
    elif not semicolon_style_double and not semicolon_style_single:
        raise exceptions.ShallNeverHappen("Cannot parse file, neither single nor double quotes are used. Invalid tailwind.config.js")
    semicolon = '"' if semicolon_style_double else "'"
    return semicolon


def parse(path: Path, prefix: str) -> str:
    _bytes: io.BytesIO = read(path)
    content = _bytes.getvalue().decode("utf-8")

    semicolon = get_semicolon_style(content)

    old_prefix = ''.join(r[0] for r in findall("prefix: {},\n", content)).strip(semicolon)
    if old_prefix and prefix != old_prefix:
        log.info(f"Found old prefix: {old_prefix} - replacing..")
        new_content = re.sub(f"prefix: {semicolon}{old_prefix}{semicolon}", f"prefix: {semicolon}{prefix}{semicolon}", content)
    elif prefix == old_prefix:
        log.info(f"The old prefix is already: {old_prefix}, skipping..")
        return old_prefix
    else:
        log.info(f"Adding prefix {prefix} to tailwind.config.js..")
        lines = content.splitlines()
        lines.insert(1, f"  prefix: {semicolon}{prefix}{semicolon},")
        new_content = "\n".join(lines)

    write(path=path, bytes=new_content.encode('utf-8'))
    return old_prefix
