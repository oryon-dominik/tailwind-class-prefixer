import logging
import re

import httpx

from ..config import settings
from ..inout import json
from .. import exceptions

log = logging.getLogger("application")


def scrape():
    """
    Scrape the tailwind classes from the official tailwind source.
    Parse possible class names to list.
    Export to json-file.
    """
    classes = []
    for url in settings.TAILWIND_CLASSES_SRC_URLS:
        try:
            r = httpx.get(url.uri)
            r.raise_for_status()
        except httpx.RequestError as exc:
            log.error(f"An error occurred while requesting {exc.request.url!r}.")
            return
        except httpx.HTTPStatusError as exc:
            log.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            return

        match url.typ:
            case "core":
                classes.extend(classes_from_source(r.content.decode("utf-8")))
            case "test":
                classes.extend(classes_from_test_source(r.content.decode("utf-8")))
            case _:
                raise exceptions.ShallNeverHappen("This type of URI is not supported.")
    
    return json.write_json_to_file(path=settings.TAILWIND_CLASSES_JSON_PATH, content=list(set(classes)))

def classes_from_source(file_content: str) -> list:
    """
    Parse the tailwind classes from the source content.

    return the list of class names
    """
    pattern = "\'\.(.*)\'"
    raw = re.findall(pattern, file_content)
    tailwind_classes = [c.split("'")[0].split()[0] for c in raw if not (c.startswith('/') or c.startswith('./'))]
    minimized = minimize_classes(tailwind_classes, keep_longest_strain=True)
    return list(sorted(minimized))

def classes_from_test_source(file_content: str) -> list:
    """
    Parse the tailwind classes from the source content.

    return the list of class names
    """
    pattern = 'class="(.*)"'
    classes_with_vars = re.findall(pattern, file_content)
    tailwind_classes = [tw_class.replace('-[var(--any-value)]', '') for tw_class in classes_with_vars]
    minimized = minimize_classes(tailwind_classes)
    return list(sorted(minimized))

def minimize_classes(tailwind_classes: list, keep_longest_strain: bool = False):
    """
    Minimize the list of tailwind classes to remove the classes duplicates and
    leave it with the stems.
    """
    minimized = []
    for _class in sorted(tailwind_classes):
        try:
            stem = _class.split("-")[0]
        except IndexError:
            stem = _class
        if stem in minimized or not stem or not _class:
            continue

        if keep_longest_strain:
            minimized.append(stem)
        else:
            minimized.append(_class)
    return minimized
