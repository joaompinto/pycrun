import typer

from .cli import cmd_run, main


def app_main():
    app = typer.Typer(short_help="Utility to manage a pypy.org metadata cache")

    app.command()(cmd_run.run)
    app.callback()(main.main)
    app()


if __name__ == "__main__":
    app_main()
