import logging
import io
import re

from bs4 import BeautifulSoup

from . import tailwind


log = logging.getLogger("application")


def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str):
    """
    Replace the old prefix or add a prefix to all classes eligible.
    An eligible class is every prefixed or unprefixed tailwind class.
    """
    prefixes = tailwind.prefixes(prefix=old_prefix)
    template = bytes.getvalue().decode("utf-8")
    soup = BeautifulSoup(template, "html.parser")

    classes = []
    for match in re.findall(r"(?<=class=\")([^\"]+)", template):
        classes.extend(match.split())

    matches = []
    for prefix in prefixes:
        matches.extend([c for c in classes if c.startswith(prefix)])

    for klass in matches:
        # normal classes like 'class'
        for tag in soup.find_all(True):
            if tag.has_attr('class') and [c for c in tag['class'] if klass in c]:
                classes = [c for c in tag['class'] if not c.startswith(klass)]
                tag['class'] = sorted(classes + [f"{new_prefix}{klass.lstrip(old_prefix)}"])

        # colon classes like ':class'
        # HACK: getting the colon classes of the disjunct from all - :class es that are empty (non-existing)
        colon_classes = list(set(list(soup.find_all())) - set(list(soup.find_all(attrs={":class": ''}))))
        for tag in colon_classes:
            if klass in tag.attrs[':class']:
                classes = [c for c in tag.attrs[':class'].split() if not c.startswith(klass)]
                tag.attrs[':class'] = ' '.join(sorted(classes + [f"{new_prefix}{klass.lstrip(old_prefix)}"]))

    return soup.prettify(formatter="html5")
