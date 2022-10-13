import logging
import re

import httpx

from ..config import settings
from ..inout import json


log = logging.getLogger("application")


def scrape():
    """
    Scrape the tailwind classes from the official tailwind source.
    Parse possible class names to list.
    Export to json-file.
    """
    try:
        r = httpx.get(settings.TAILWIND_CLASSES_SRC_URL)
        r.raise_for_status()
    except httpx.RequestError as exc:
        log.error(f"An error occurred while requesting {exc.request.url!r}.")
        return
    except httpx.HTTPStatusError as exc:
        log.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return

    classes = get_classes_from_source(r.content.decode("utf-8"))
    return json.write_json_to_file(path=settings.TAILWIND_CLASSES_JSON_PATH, content=classes)

def get_classes_from_source(file_content: str) -> list:
    """
    Parse the tailwind classes from the source content.

    return the list of class names
    """
    pattern = 'class="(.*)"'
    classes_with_vars = re.findall(pattern, file_content)
    tailwind_classes = [tw_class.replace('-[var(--any-value)]', '') for tw_class in classes_with_vars]
    log.debug(len(tailwind_classes))
    return list(sorted(tailwind_classes))
