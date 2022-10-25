import logging
import io
import re


import parse as parse_official

from . import tailwind
from . import prefix

log = logging.getLogger("application")





def match_regex(match: re.Match) -> str:
    """Replace the old prefix or add a prefix to all classes eligible."""
    prefix = prefix.cache()
    prefixes = tailwind.prefixes(prefix=prefix.old)
    classes = parse_official.parse(format='class:"{}"', string=match.group())[0].split()
    matches = tailwind.match_classes(classes=classes, prefixes=prefixes)
    replaced = [
        tailwind.build_replacement(prefix=prefix, klass=klass)
        if klass in matches else klass
        for klass in classes
    ]
    return 'class:"' + ' '.join(replaced) + '"'


def parse(bytes: io.BytesIO, prefix: prefix.Prefix) -> str:
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.

    Probably makes most sense in post build javascript files.
    """
    prefix.cache(prefix=prefix)
    template = bytes.getvalue().decode("utf-8")
    regex = re.compile(r"class\:\"([^\"]+)\"", re.S)
    return regex.sub(repl=match_regex, string=template)
