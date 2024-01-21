"""Script containing common variables and functions for Typer CLI."""
import time
from enum import Enum
from pathlib import Path

import httpx
import typer
from rich.console import Console

epilog = r"[dim]Made by [bold blue]IML Team[/bold blue] under MIT License[/dim]"

console = Console()
verbose_console = Console(stderr=True, style="yellow")
err_console = Console(stderr=True, style="bold red")


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


def validate_file_location(location: Path | None) -> Path:
    if location is None:
        err_console.print("Please, provide file path with --file-location")
        raise typer.Exit(code=1)

    if (
        location.is_socket()
        or location.is_fifo()
        or location.is_block_device()
        or location.is_char_device()
    ):
        err_console.print(f"The given path {location} does not point to a regular file.")
        raise typer.Exit(code=1)

    if location.is_symlink():
        console.print(f"Careful, {location} is a symlink, not a file", style="yellow")

    return location


def print_json(console: Console, text: str = "", *, data: dict | None = None):
    _style = err_console.style
    console.style = "black"

    if text:
        console.print_json(text)
    elif data:
        console.print_json(data=data)
    else:
        raise ValueError("Either 'text' or 'data' must be provided")

    console.style = _style


def raise_exception():
    """Sleep 2 seconds and raise exception"""
    time.sleep(2)

    message: str = (
        "Client error '422 Unprocessable Entity' for url"
        "'http://localhost:44681/sample/1?name=test'\nFor more information check:"
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422"
    )

    request: httpx.Request = httpx.Request(
        method="POST",
        url="http://localhost:44681/sample/1?name=test",
    )

    response: httpx.Response = httpx.Response(
        status_code=422,
        json={
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "num"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
            ]
        },
    )
    raise httpx.HTTPStatusError(message, request=request, response=response)


__all__ = [
    "epilog",
    "console",
    "verbose_console",
    "err_console",
]
