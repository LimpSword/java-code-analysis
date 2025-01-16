import os
import subprocess

import typer

from cli.pmd import require_pmd

app = typer.Typer()

rules_file = "java-rules.xml"


@app.command()
def analyze(folder: str):
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
    subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    print(f"Analysis report saved to {sanitized_folder}.html")


@app.command()
def analyze_all(folder: str):
    """
    Analyze all projects in the given folder.
    """
    pmd = require_pmd()
    if not pmd:
        raise typer.Exit()

    print(f"Analyzing all projects in folder: {folder}")
