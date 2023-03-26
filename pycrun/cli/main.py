import typer
from metadict import MetaDict

state = MetaDict({"verbose": False})


def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode")
):
    """
    Utility to manage a pypi.org metadata cache
    """
    if verbose:
        state["verbose"] = True
