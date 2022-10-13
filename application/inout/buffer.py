import io
from pathlib import Path

import typer


def get_file_buffer(path: Path) -> io.BytesIO:
    """
    Get file buffer from path or raise a typer error.
    """
    if not path.exists():
        typer.echo(f"File {path.name} not found", err=True)
        raise typer.Exit()
    return io.BytesIO(path.read_bytes())


def write_bytes_to_file(path: Path, bytes: io.BytesIO) -> None:
    """
    Write byte content to file.
    """
    return path.write_bytes(bytes)
