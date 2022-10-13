#!/usr/bin/env python3
# coding: utf-8

"""Command Line Interface for adding or changing tailwind prefix classes in an existing project."""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console


from application import __application__, __version__

from application.config import settings
from application.config.logs import logging

log = logging.getLogger('application')
console = Console()
print = console.print
cli = typer.Typer(no_args_is_help=True)


def _version_callback(value: bool) -> None:
    """Print version."""
    if value:
        print(f"{__application__}: {__version__}")
        raise typer.Exit()


@cli.command()
def update():
    """Update the tailwind class list from official sources."""
    # httpx.get and parse to list..
    ...

@cli.command()
def prefix(
        path: Path = typer.Argument(None, help="Path to project root."),
        prefix: Optional[str] = typer.Argument(
            settings.TAILWIND_DEFAULT_PREFIX,
            help="Change the prefix for tailwind classes.",
        ),
    ):
    """Process an existing project."""
    if not path.exists():
        print(f"Please provide a valid path to an existing vue project.", style="red")
        raise typer.Exit()
    from application.parser import walk
    walk.tree(path)

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
    # print(f"Prefixing project with {settings.TAILWIND_DEFAULT_PREFIX}")
    return None


def main():
    cli(prog_name=__application__)

if __name__ == "__main__":
    main()
