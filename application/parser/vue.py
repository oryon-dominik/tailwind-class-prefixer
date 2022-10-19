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
    soup = BeautifulSoup(template, "html.parser")

    classes = []
    for match in re.findall(r"(?<=class=\")([^\"]+)", template):
        classes.extend(match.split())
    classes = tailwind.join_classbindings(classes=classes)
    matches = tailwind.match_classes(classes=classes, prefixes=prefixes)

    for klass in matches:
        # normal classes like 'class'
        for tag in soup.find_all(True):
            css_classes = tag.get('class', [])
            if css_classes and [c for c in css_classes if klass in c]:
                assert tag.has_attr('class'), "Tag has no class attribute?! This should not happen."
                non_used = [c for c in css_classes if c != klass]
                replacement = tailwind.build_replacement(old_prefix=old_prefix, new_prefix=new_prefix, klass=klass)
                tag['class'] = list(set(sorted(non_used + [replacement])))

        # colon classes like ':class'
        # HACK: getting the colon classes of the disjunct from all - :class es that are empty (non-existing)
        colon_classes = list(set(list(soup.find_all())) - set(list(soup.find_all(attrs={":class": ''}))))
        for tag in colon_classes:
            if klass in tag.attrs[':class']:
                css_classes = tag.attrs[':class'].split()
                # print(f'>>> DEBUG: {css_classes=} {tag=}')
                non_used = [c for c in css_classes if c != klass]
                # special case: if the class is a media query, we need to keep the media query
                replacement = tailwind.build_replacement(old_prefix=old_prefix, new_prefix=new_prefix, klass=klass)
                tag.attrs[':class'] = ' '.join(list(set(sorted(non_used + [replacement]))))

    return soup.prettify(formatter="html5")
