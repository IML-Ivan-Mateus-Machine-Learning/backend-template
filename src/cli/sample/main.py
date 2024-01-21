"""Script containing sample of Typer CLI."""
import datetime as dt
from pathlib import Path
from typing import Annotated
from typing import Union

import httpx
import typer
from common import NeuralNetwork
from common import console
from common import epilog
from common import err_console
from common import print_json
from common import raise_exception
from common import validate_file_location
from common import verbose_console

app = typer.Typer(
    name="Sample CLI",
    add_completion=False,
    rich_markup_mode="rich",
    epilog=epilog,
)

state = {"verbose": False}


# Sample command with lots of different parameters and features
@app.command(
    name="run_me",
    help="A command with most common typer features.",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    epilog=epilog,
)
def this_name_is_replaced_by_name_in_command_decorator(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
    age: Annotated[int, typer.Option(prompt="How old are you?", min=18)] = 21,
    truth: Annotated[Union[bool, None], typer.Option("--truth/--lie", "-t/-f")] = None,
    date_reference: Annotated[
        Union[dt.datetime, None],
        typer.Option(
            rich_help_panel="",
            help=r"[dim]\[default: today][/dim]",
            show_default=False,
            formats=["%Y-%m-%d"],
        ),
    ] = None,
    network: Annotated[NeuralNetwork, typer.Option(case_sensitive=False)] = NeuralNetwork.simple,
    file_location: Annotated[
        Union[Path, None],
        typer.Option(exists=True, file_okay=True, dir_okay=False),
    ] = None,
    error: Annotated[
        bool, typer.Option("--error", "-e", is_flag=True, help="Force raising an exception.")
    ] = False,
):
    """A command with most common typer features."""
    # Get default value from a function
    date_reference = (date_reference or dt.datetime.now()).date()

    # Custom validation of parameter
    file_location: Path = validate_file_location(file_location)

    if error:
        try:
            with console.status("Generating sample exception", spinner="arc"):
                raise_exception()
        except httpx.HTTPStatusError as exc:
            err_console.print_exception()
            print_json(err_console, data=exc.response.json())

            raise typer.Exit(code=1) from exc

    console.print(
        f"Hello {name} ({age} y.o.) {truth} at {date_reference} with {network.value}.\n"
        f"File located at {file_location} contains {file_location.stat().st_size} chars."
    )


@app.callback(
    invoke_without_command=True,
)
def main(
    ctx: typer.Context,
    verbose: Annotated[bool, typer.Option("--verbose")] = False,
):
    """
    Sample CLI.
    """
    # Custom message if no command is provided
    if ctx.invoked_subcommand is None:
        err_console.log("Please, specify a command.")
        ctx.get_help()
        raise typer.Exit(code=1)

    # Forward verbose state to commands
    state["verbose"] = verbose

    # Disable the verbose console if verbose is not set
    verbose_console.quiet = not verbose

    verbose_console.log(f"About to execute command: [bold]{ctx.invoked_subcommand}[/bold]")


if __name__ == "__main__":
    app()
