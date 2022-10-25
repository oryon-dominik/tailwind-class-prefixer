"""Will get imported via __init__.py on module level"""
import secrets

from functools import lru_cache
from dataclasses import dataclass
from typing import Literal

# order matters!
from .paths import ROOT_DIR
from . import logs


@lru_cache()
def get_settings():
    """
    Get settings from config.
    @Least-recently-used cache decorator.
    -> Return the same value that was returned the first time, instead of computing it again.
    """
    return Settings(**{})


@dataclass
class URL:
    """URL from the offical sources with types to process"""
    typ: Literal["core", "test"]
    uri: str  # -> URL type


class Settings:
    """
    Settings for the application.

    Use Typehints to ensure your IDE will moan, if the types get messed up.
    """

    # -> https://blog.miguelgrinberg.com/post/the-new-way-to-generate-secure-tokens-in-python
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # logging
    LOG_LEVEL = logs.LOG_LEVEL

    TAILWIND_DEFAULT_PREFIX = "tw-"
    ALLOWED_FILE_EXTENSIONS = [".vue", ".css", ".js", ".html"]
    IGNORE_DIRECTORIES = [".git", "__pycache__", "node_modules", "dist", "build", "public", "static"]

    TAILWIND_CLASSES_SRC_URLS = [
        URL(typ="core", uri="https://raw.githubusercontent.com/tailwindlabs/tailwindcss/master/src/corePlugins.js"),
        URL(typ="test", uri="https://raw.githubusercontent.com/tailwindlabs/tailwindcss/master/tests/any-type.test.js"),
    ]
    TAILWIND_CLASSES_JSON_PATH = ROOT_DIR / "tailwind-classes" / "tailwind-classes-list.json"
    TAILWIND_CONFIG_FILENAME = "tailwind.config.js"
