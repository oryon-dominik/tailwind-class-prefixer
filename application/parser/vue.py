import logging
import io
import re

from .tailwind import get_tailwind_classes_list

log = logging.getLogger("application")

def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str):
    classes = get_tailwind_classes_list()
    template = bytes.getvalue().decode("utf-8")
    # TODO: implement replacing the new prefix with the old prefix or adding the prefix to all classes
    for _class in classes:
        old_name = f"{old_prefix}{_class}"
        new_name = f"{new_prefix}{old_name.lstrip(old_prefix)}"
        # find matches inside the class or :class pattern
        # - replace these with        
        # re.sub(old_name, new_name)
