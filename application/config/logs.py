import logging
import logging.config

from .paths import ROOT_DIR

logs_path = ROOT_DIR / "logs"
logs_path.mkdir(exist_ok=True)

LOG_LEVEL = logging.INFO
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{levelname}:     [{asctime}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format": "{levelname}  [{asctime}] \t Module: {module} \t Logger: {name} \t Process: {process:d} \t Thread: {thread:d}\n      {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "rich": {
            "format": "{message}",
            "style": "{",
            "datefmt": "[%X]",
        },
        "rich_with_loggername": {
            "format": "{name}: {message}",
            "style": "{",
            "datefmt": "[%X]",
        },
        "rich_verbose": {
            "format": "{message} \nLogger: {name} | Process: {process:d} | Thread: {thread:d}",
            "style": "{",
            "datefmt": "[%X]",
        },
    },
    "handlers": {
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "level": LOG_LEVEL,
            "formatter": "rich",
        },
        "rich_console_with_loggername": {
            "class": "rich.logging.RichHandler",
            "level": LOG_LEVEL,
            "formatter": "rich_with_loggername",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": LOG_LEVEL,
            "formatter": "default",
            "filename": str(logs_path / "application.log"),
        },
    },
    "loggers": {
        "application": {
            "handlers": ["rich_console", "file"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}
# apply the config
logging.config.dictConfig(LOGGING)
