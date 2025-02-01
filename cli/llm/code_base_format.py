from dataclasses import dataclass
from typing import List


@dataclass
class ImprovementPoint:
    problem: str
    example_in_project: str
    solution: str
    why: str


@dataclass
class GoodPractice:
    description: str


@dataclass
class SoftwareArchitecture:
    system_prompt = """You are a software architect in charge of giving feedback on the software architecture of a Java code base of a JavaFX project. 
    The code base has been developed by four students during a week-long school project. You are focused on the Java part rather than the JavaFX part."""
    prompt = """
    Code base:
    {code_base}
    ----

    Analyze this code base and carefully write every semantic mistake you find in the code. The code should be as clear
    and as maintainable as possible and should follow the best practices of software architecture. Rules should not be
    too strict, as the students are still learning. Give as many improvement points as relevant. Note that the code you
    review may be part of a larger project, so you should consider as much as you can about the context of the code.
    At the root, you have a PMD report that you can use to help you analyze the code base. Keep any comments about it
    in the PMD Static Analysis Summary section.
    """

    name: str
    description: str
    improvement_points: List[ImprovementPoint]
    good_practices: List[GoodPractice]
    pmd_static_analysis_summary: str
    final_summary: str

    def to_markdown(self) -> str:
        lines = [
            f"# {self.name}\n",
            f"\n{self.description}\n\n",
        ]
        for i, point in enumerate(self.improvement_points):
            lines.append(f"## Improvement Point {i + 1}\n")
            lines.append(f"\n**Problem**: {point.problem}\n")
            lines.append(f"\n**Example**: {point.example_in_project}\n")
            lines.append(f"\n**Solution**: {point.solution}\n")
            lines.append(f"\n**Why**: {point.why}\n")
        lines.append("\n")
        lines.append("## Good Practices\n")
        for i, practice in enumerate(self.good_practices):
            lines.append(f"**{i + 1}.** {practice.description}\n\n")
        lines.append("\n")
        lines.append("## PMD Static Analysis Summary\n")
        lines.append(f"{self.pmd_static_analysis_summary}\n")
        lines.append("## Summary\n")
        lines.append(f"{self.final_summary}\n")
        return "".join(lines)
