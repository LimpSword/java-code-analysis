from dataclasses import dataclass
from typing import List


@dataclass
class ImprovementPoint:
    problem: str
    solution: str
    example: str
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
    and as maintainable as possible and should follow the best practices of software architecture. However, no need to
    be too strict, as the students are still learning.
    """

    name: str
    description: str
    improvement_points: List[ImprovementPoint]
    good_practices: List[GoodPractice]
    summary: str

    def to_markdown(self) -> str:
        lines = [
            f"# {self.name}\n",
            f"\n{self.description}\n\n",
        ]
        for i, point in enumerate(self.improvement_points):
            lines.append(f"## Improvement Point {i + 1}\n")
            lines.append(f"\n**Problem**: {point.problem}\n")
            lines.append(f"\n**Solution**: {point.solution}\n")
            lines.append(f"\n**Example**: {point.example}\n")
            lines.append(f"\n**Why**: {point.why}\n")
        lines.append("\n")
        lines.append("## Good Practices\n")
        for i, practice in enumerate(self.good_practices):
            lines.append(f"**{i + 1}.** {practice.description}\n\n")
        lines.append("\n")
        lines.append("## Summary\n")
        lines.append(f"{self.summary}\n")
        return "".join(lines)
