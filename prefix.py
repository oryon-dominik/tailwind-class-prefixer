#!/usr/bin/env python3
# coding: utf-8

"""Command Line Interface for adding or changing tailwind prefix classes in an existing project."""
from pathlib import Path
from typing import Optional

import typer

from application import __application__, __version__

from application.config import settings
from application.config.logs import logging

log = logging.getLogger('application')
cli = typer.Typer(no_args_is_help=True)


def _version_callback(value: bool) -> None:
    """Print version."""
    if value:
        log.info(f"{__application__}: {__version__}")
        raise typer.Exit()


@cli.command()
def update():
    """Update the tailwind class list from official sources."""
    from application.update import repository
    classes = repository.scrape()
    log.info(f"Tailwind classes scraped: {classes}")


@cli.command()
def prefix(
        path: Path = typer.Argument(None, help="Path to project root."),
        prefix: Optional[str] = typer.Argument(
            settings.TAILWIND_DEFAULT_PREFIX,
            help="Change the prefix for tailwind classes.",
        ),
    ):
    """Process an existing project."""
    if path is None or not path.exists():
        log.error(f"Please provide a valid path to an existing vue project.")
        raise typer.Exit()

    from application.parser import walk
    walk.search(path=path, prefix=prefix)


@cli.callback()
def callback(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,  # processed upfront!
        ),
    ) -> None:
    __file__.__doc__
    # This will run before all commands:
    # log.info(f"Prefixing project with {settings.TAILWIND_DEFAULT_PREFIX}")
    return None


def main():
    cli(prog_name=__application__)

if __name__ == "__main__":
    main()
