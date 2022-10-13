import logging
import io

log = logging.getLogger("application")

def parse(bytes: io.BytesIO):
    log.info(bytes.getvalue())
