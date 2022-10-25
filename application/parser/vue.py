import logging
import io
import re

import parse as parse_official

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

    # classes = parse_official.parse(format='class="{}"', string=match.group())[0].split()
    regex = re.compile(r"class\:\"([^\"]+)\"", re.S)


    # classes = []
    # for match in re.findall(r"(?<=class=\")([^\"]+)", template):
    #     classes.extend(match.split())
    # classes = tailwind.join_classbindings(classes=classes)
    # matches = tailwind.match_classes(classes=classes, prefixes=prefixes)

    # for klass in matches:
    #     # normal classes like 'class'
    #     for tag in soup.find_all(True):
    #         css_classes = tag.get('class', [])
    #         if css_classes and [c for c in css_classes if klass in c]:
    #             assert tag.has_attr('class'), "Tag has no class attribute?! This should not happen."
    #             non_used = [c for c in css_classes if c != klass]
    #             replacement = tailwind.build_replacement(old_prefix=old_prefix, new_prefix=new_prefix, klass=klass)
    #             tag['class'] = list(set(sorted(non_used + [replacement])))

    #     # colon classes like ':class'
    #     # HACK: getting the colon classes of the disjunct from all - :class es that are empty (non-existing)
    #     colon_classes = list(set(list(soup.find_all())) - set(list(soup.find_all(attrs={":class": ''}))))
    #     for tag in colon_classes:
    #         if klass in tag.attrs[':class']:
    #             css_classes = tag.attrs[':class'].split()
    #             css_classes = tailwind.join_classbindings(classes=css_classes)
    #             non_used = [c for c in css_classes if c != klass and not (tailwind.is_classbinding(c) and klass in c)]
                
    #             # handle classbindings differently
    #             _klass = klass
    #             class_bindings = [c for c in css_classes if tailwind.is_classbinding(c) and klass in c]
    #             if class_bindings:
    #                 _klass = class_bindings[0]
    #             replacement = tailwind.build_replacement(old_prefix=old_prefix, new_prefix=new_prefix, klass=_klass)
    #             tag.attrs[':class'] = ' '.join(list(set(sorted(non_used + [replacement]))))

    return template # soup.prettify(formatter="html5")  # prettify destroys several vue js layout decisions
