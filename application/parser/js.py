import logging
import io
import re

import parse as parse_official

from . import tailwind


log = logging.getLogger("application")

GLOBALS = {
    "old_prefix": "",
    "new_prefix": "",
    "count": 0,
}


def match_regex(match: re.Match, old_prefix: str = GLOBALS["old_prefix"], new_prefix: str = GLOBALS["new_prefix"]) -> str:
    """Replace the old prefix or add a prefix to all classes eligible."""
    prefixes = tailwind.prefixes(prefix=old_prefix)
    classes = parse_official.parse(format='class:"{}"', string=match.group())[0].split()
    matches = tailwind.match_classes(classes=classes, prefixes=prefixes)
    replaced = [
        tailwind.build_replacement(old_prefix=old_prefix, new_prefix=new_prefix, klass=klass)
        if klass in matches else klass
        for klass in classes
    ]
    return 'class:"' + ' '.join(replaced) + '"'


def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str) -> str:
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.
    """
    
    template = bytes.getvalue().decode("utf-8")

    regex = re.compile(r"class\:\"([^\"]+)\"", re.S)

    GLOBALS["old_prefix"] = old_prefix
    GLOBALS["new_prefix"] = new_prefix

    template = regex.sub(repl=match_regex, string=template)
        # print(f'>>> DEBUG: {count=}, {prefix=}, {replacement=}')

    # print(f'>>> DEBUG: {template=}')
    return template
