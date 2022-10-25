import logging
import io
import re

from . import tailwind
from .prefix import Prefix

log = logging.getLogger("application")


def parse(bytes: io.BytesIO, prefix: Prefix) -> str:
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.
    """
    prefixes = tailwind.prefixes(prefix=prefix.old)
    template = bytes.getvalue().decode("utf-8")

    for prfx in prefixes:
        dot_new = f".{prefix.new}{prfx.removeprefix(prefix.old)}"
        template = re.sub(fr"\.{prfx}", dot_new, template)
        space_new = f" {prefix.new}{prfx.removeprefix(prefix.old)}"
        template = re.sub(fr"\s{prfx}", space_new, template)

    return template
