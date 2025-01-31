import os
import subprocess
from typing import Annotated

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli.pmd import require_pmd

from cli.llm.llm_analysis import analyze_code_base, summarize_projects

app = typer.Typer()

rules_file = "java-rules.xml"


@app.command()
def analyze(folder: Annotated[str, typer.Argument()], llm: Annotated[
    bool, typer.Option("--llm/--no-llm", help="Analyze the code base with the LLM assistant")] = False,
            model: Annotated[str, typer.Argument()] = None):
    """
    Analyze the given project folder.
    """
    pmd = require_pmd()
    if not pmd:
        raise typer.Exit()

    # TODO: Do that for Windows

    # Find src/main/java folder in the given project folder
    right_path = ""
    for root, dirs, files in os.walk(folder):
        if "src" in dirs:
            src_path = os.path.join(root, "src", "main", "java")
            if os.path.exists(src_path):
                right_path = src_path
                break

    print("Found src/main/java folder at:", right_path)

    print(f"Analyzing folder: {folder}")
    sanitized_folder = folder.replace('/', '.')
    command = f"pmd check --no-cache -d {right_path} -R {rules_file} -f html -r {sanitized_folder}.html"

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Analyzing code base...", total=1)
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        progress.update(task, completed=1)

    print(f"Analysis report saved to {sanitized_folder}.html")

    if llm:
        html_file = f"{sanitized_folder}.html"
        dest = os.path.join(folder, html_file)
        subprocess.run(f"cp {html_file} {dest}", shell=True, stdout=subprocess.PIPE)

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Analyzing code base with an LLM assistant...", total=1)
            analyze_code_base(folder, save_file=True, model=model)
            progress.update(task, completed=1)
            print("Analysis report saved to output folder.")


@app.command()
def analyze_all(folder: str):
    """
    Analyze all projects in the given folder.
    """
    pmd = require_pmd()
    if not pmd:
        raise typer.Exit()

    print(f"Analyzing all projects in folder: {folder}")

    for project in os.listdir(folder):
        project_folder = os.path.join(folder, project)
        if os.path.isdir(project_folder):
            analyze(project_folder)

    print("All projects analyzed.")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Summarizing projects...", total=1)
        summarize_projects()
        progress.update(task, completed=1)

    print("Summary saved to output folder.")
