import logging
import io
import re

from .tailwind import get_tailwind_classes_list

log = logging.getLogger("application")

def parse(bytes: io.BytesIO, new_prefix: str, old_prefix: str):
    classes = get_tailwind_classes_list()
    template = bytes.getvalue().decode("utf-8")
    # TODO: implement replacing the new prefix with the old prefix or adding the prefix to all classes
    
    # from rich import print
    
    # for tw_class in classes:
        
        
        # find matches inside the class or :class pattern
        
        # TODO: -> :class
        # current_classes = re.findall(r"(?<=class=\")([^\"]+)", template)
        # for _klass in current_classes:
            # if tw_class in _klass:
                # matches = re.findall(fr"({old_prefix}{tw_class}).*", _klass)
                # print(f'>>> DEBUG: {matches}')
                # old_name = fr"({old_prefix}{tw_class}"
                # new_name = f"{new_prefix}{old_name.lstrip(old_prefix)}"
                
                # print(f'>>> DEBUG: {tw_class=} {_klass=} {old_name=} {new_name=}')
                
                # _klass
                # res = re.sub(f'{_klass}', f'{new_name}', current_classes[0])
                # print(res)

    
    # print(f'{template}')
    # TODO: write template
