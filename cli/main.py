import typer

from .analysis import app as analysis_app

app = typer.Typer()

app.add_typer(analysis_app)

if __name__ == "__main__":
    app()
