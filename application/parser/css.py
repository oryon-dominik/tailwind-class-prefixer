import logging
import io
import re

from bs4 import BeautifulSoup

from . import tailwind


log = logging.getLogger("application")


def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str) -> str:
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.
    """
    prefixes = tailwind.prefixes(prefix=old_prefix)
    template = bytes.getvalue().decode("utf-8")

    for prefix in prefixes:
        dot_new = f".{new_prefix}{prefix.removeprefix(old_prefix)}"
        template = re.sub(fr"\.{prefix}", dot_new, template)
        space_new = f" {new_prefix}{prefix.removeprefix(old_prefix)}"
        template = re.sub(fr"\s{prefix}", space_new, template)

    return template
