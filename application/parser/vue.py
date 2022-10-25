import logging
import io
import re

import parse as parse_official

from . import tailwind
from . import prefix as pfx

log = logging.getLogger("application")


def match_regex(match: re.Match) -> str:
    """Replace the old prefix or add a prefix to all classes eligible."""
    prefix = pfx.cache()
    prefixes = tailwind.prefixes(prefix=prefix.old)
    classes: str = parse_official.parse(format='class="{}"', string=match.group())[0]

    built = tailwind.build_classes(classes=classes)
    matches = tailwind.match_classes(classes=built, prefixes=prefixes)

    replaced = [
        tailwind.build_replacement(prefix=prefix, klass=klass)
        if klass in matches else klass
        for klass in built
    ]
    return f'class="{"".join(replaced)}"'


def parse(bytes: io.BytesIO, prefix: pfx.Prefix) -> str:
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.
    """
    template = bytes.getvalue().decode("utf-8")
    pfx.cache(prefix=prefix)
    regex = re.compile(r"class=\"([^\"]+)\"", re.S)
    return regex.sub(repl=match_regex, string=template)
