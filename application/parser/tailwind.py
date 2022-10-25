import logging
import io
import re
import string
from pathlib import Path

from parse import findall

from ..config import settings
from ..inout import read, write, json
from .. import exceptions
from .prefix import Prefix


log = logging.getLogger("application")


def is_classbinding(klass: str) -> bool:
    """Assume a stripped class is a classbinding if braces are found around it."""
    klass = klass.strip()
    return klass.startswith('{') and klass.endswith('}')


def build_classes(classes: str) -> list:
    """Build a list of all classes from the tailwind.config.js file."""
    built = []
    word = ""
    for char in classes:
        if char in list(string.ascii_letters) + list(string.digits) + ['-']:
            word += char
        else:
            if word:
                built.append(word)
                word = ""
            built.append(char)
    if word:
        built.append(word)
    return built


def build_replacement(prefix: Prefix, klass: str) -> str:
    """
    Return a replacement string for the tailwind class used.
    Including class bindings ':class'.
    """
    if is_classbinding(klass):
        # special case: if the class is a classbinding, keep the class intact
        class_binding = klass.split(':')[0].removeprefix('{').strip()
        replacement = f"{prefix.new}{class_binding.removeprefix(prefix.old)}"
        return klass.replace(class_binding, replacement)
    elif ':' in klass:
        # special case: if the class is a media query, we need to keep the media query
        media_query, name = klass.split(':')
        return f"{media_query}:{prefix.new}{name.removeprefix(prefix.old)}"
    return f"{prefix.new}{klass.removeprefix(prefix.old)}" 


def match_classes(classes: list, prefixes: list) -> list:
    matches = []
    for prefix in prefixes:
        # normal classes
        pure_classes = [c for c in classes if ':' not in c]
        pure_classes = [c for c in pure_classes if c.startswith(prefix)]
        matches.extend(pure_classes)
        # media queries
        media_query_classes = [c for c in classes if ':' in c]
        media_query_classes = [c for c in media_query_classes if c.split(':')[1].startswith(prefix)]
        matches.extend(media_query_classes)
        # classbindings
        classbinding_classes = [c for c in classes if '{' in c and '}' in c]
        classbinding_classes = [c.split(':')[0].removeprefix('{').strip() for c in classbinding_classes]
        classbinding_classes = [c for c in classbinding_classes if c.startswith(prefix)]
        matches.extend(classbinding_classes)
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
            classbindings = []
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
    prefixed = [
        f"{prefix}{klass}"
        for prefix in list(set([prefix, ""]))
        for klass in classes()
    ]
    appended = [f"{c}-" for c in prefixed]
    return appended + prefixed


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
    """
    Parse the tailwind.config.js and replace all tailwind classes with the given prefix.
    """
    assert path.name == settings.TAILWIND_CONFIG_FILENAME, f"Filename {path.name} is not {settings.TAILWIND_CONFIG_FILENAME}."
    _bytes: io.BytesIO = read(path)
    content = _bytes.getvalue().decode("utf-8")

    has_prefix: bool = "prefix:" in content
    semicolon = semicolon_style(content)

    prefixes = findall("prefix: {},\n", content)
    old_prefix = ''.join(r[0] for r in prefixes).strip(semicolon)

    if has_prefix and prefix != old_prefix:
        log.info(f"Found old prefix: '{old_prefix}' - replacing with '{prefix}'..")
        new_content = re.sub(f"prefix: {semicolon}{old_prefix}{semicolon}", f"prefix: {semicolon}{prefix}{semicolon}", content)
    elif prefix == old_prefix:
        return old_prefix
    else:
        log.info(f"Adding prefix '{prefix}' to tailwind.config.js..")
        lines = content.splitlines()
        if not any([f"prefix:" in l for l in lines]):
            module = lines.index("module.exports = {")
            lines.insert(module + 1, f"  prefix: {semicolon}{prefix}{semicolon},")
        new_content = "\n".join(lines)

    write(path=path, bytes=new_content.encode('utf-8'))
    return old_prefix
