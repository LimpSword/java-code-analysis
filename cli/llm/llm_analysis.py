from pathlib import Path

from llm_components.loaders.code_base import map_codebase_to_text
from llm_core.assistants import AnthropicAssistant

from cli.llm.code_base_format import SoftwareArchitecture
from cli.llm.summary_format import Summary

save_folder = "output"
Path(save_folder).mkdir(parents=True, exist_ok=True)


def analyze_code_base(folder: str, save_file=False) -> str:
    path = Path(folder)
    code_base = map_codebase_to_text(path)

    with AnthropicAssistant(SoftwareArchitecture) as assistant:
        software_architecture = assistant.process(code_base=code_base)
        markdown_output = software_architecture.to_markdown()

    if save_file:
        with open(f"{save_folder}/{folder}.md", "w") as f:
            f.write(markdown_output)

    return markdown_output


# To give a summary of all analyzed projects
def summarize_projects() -> str:
    reports = Path(save_folder)
    code_base_reports = map_codebase_to_text(reports)

    with AnthropicAssistant(Summary) as assistant:
        software_architecture = assistant.process(code_base=code_base_reports)
        markdown_output = software_architecture.to_markdown()

    with open(f"{save_folder}/summary.md", "w") as f:
        f.write(markdown_output)

    return markdown_output