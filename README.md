# java-code-analysis

## Description

The project uses pmd to statically analyze java code.

## Run

To analyze a project:

```bash
python -m cli.main analyze <folder>
```

By default, there is no analysis by an LLM, if you want to review the project code by an LLM, you can use the `--llm`
flag and your api key:

```bash
ANTHROPIC_API_KEY="your api key" python -m cli.main analyze <folder> --llm
```