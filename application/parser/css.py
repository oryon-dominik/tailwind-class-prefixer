import logging
import io

from .tailwind import get_tailwind_classes_list

log = logging.getLogger("application")

def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str):
    classes = get_tailwind_classes_list()
    template = bytes.getvalue().decode("utf-8")
    # TODO: implement replacing the new prefix with the old prefix or adding the prefix to all classes
