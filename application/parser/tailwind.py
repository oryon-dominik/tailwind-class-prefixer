import logging
import io
import re
from pathlib import Path

from parse import findall

from ..config import settings
from ..inout import read, write, json
from .. import exceptions


log = logging.getLogger("application")


def build_replacement(old_prefix: str, new_prefix: str, klass: str) -> str:
    if ':' in klass:
        # special case: if the class is a media query, we need to keep the media query
        media_query, name = klass.split(':')
        return f"{media_query}:{new_prefix}{name.removeprefix(old_prefix)}"
    return f"{new_prefix}{klass.removeprefix(old_prefix)}" 


def match_classes(classes: list, prefixes: list) -> list:
    matches = []
    for prefix in prefixes:
        pure_classes = [c for c in classes if ':' not in c]
        pure_classes = [c for c in pure_classes if c.startswith(prefix)]
        matches.extend(pure_classes)
        media_query_classes = [c for c in classes if ':' in c]
        media_query_classes = [c for c in media_query_classes if c.split(':')[1].startswith(prefix)]
        matches.extend(media_query_classes)
    return list(set(matches))

def join_classbindings(classes: list) -> list:
    """Join all previously split classbindings into a single str."""
    bind = False
    cleaned = []
    classbindings = []

    # differentiate between classbindings and normal classes
    for klass in classes:
        if klass == "{":
            bind = True
        if klass == "}":
            classbindings.append(klass)
            cleaned.append(" ".join(classbindings))
            bind = False
            continue

        if bind:
            classbindings.append(klass)
        elif bind is False:
            cleaned.append(klass)

    return cleaned


def prefixes(prefix=str) -> list:
    """
    Return a list of all class-prefix combinations:
        - That are non-prefixed
        - or that are prefixed with the given prefix.
    Also adding the '-' dash to class.
    """
    return [
        f"{prefix}{klass}"
        for prefix in list(set([prefix, ""]))
        for klass in [f"{c}-" for c in classes()]
    ]


def classes() -> list:
    """Read the list of all tailwind classes from json."""
    return json.load_json_from_file(path=settings.TAILWIND_CLASSES_JSON_PATH)


def semicolon_style(content: str) -> str:
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

    semicolon = semicolon_style(content)

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
        if not any([f"prefix:" in l for l in lines]):
            lines.insert(1, f"  prefix: {semicolon}{prefix}{semicolon},")
        new_content = "\n".join(lines)

    write(path=path, bytes=new_content.encode('utf-8'))
    return old_prefix
