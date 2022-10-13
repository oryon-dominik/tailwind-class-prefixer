import pytest

from typer.testing import CliRunner

from rich.text import Text

from application import __application__, __version__
from prefix import cli


runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"{__application__}: {__version__}" in Text.from_ansi(result.stdout)

def test_vue_conversion():
    # random - prefix..
    result = runner.invoke(cli, ["prefix", "./application/tests/mocks/", ""])
    assert result.exit_code == 0

    print(result.stdout)
    assert False
