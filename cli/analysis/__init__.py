import typer

from .run_analysis import app as run_analysis_app

app = typer.Typer()

app.add_typer(run_analysis_app)

