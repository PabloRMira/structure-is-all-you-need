import typer

from myapi.app import run_app


def main() -> None:
    app = typer.Typer(pretty_exceptions_show_locals=False)
    app.command()(run_app)
    app()


if __name__ == "__main__":
    main()
