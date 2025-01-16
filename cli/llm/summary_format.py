from dataclasses import dataclass
from typing import List


@dataclass
class ImprovementPoint:
    problem: str
    solution: str

@dataclass
class GoodPractice:
    description: str


@dataclass
class Summary:
    system_prompt = """You are a software architect in charge of giving feedback on the software architecture of a Java code base of a JavaFX project. 
    The code base has been developed by four students during a week-long school project. You are focused on the Java part rather than the JavaFX part."""
    prompt = """
    You have received those reports from the other reviewers. You are in charge of summarizing the reports and giving a general feedback on the software architecture of the projects.
    The report should be as exhaustive as possible and should give a clear idea of the quality of the software architecture of the projects.
    It should give students a clear idea of what they did well and what they need to improve.
    """

    name: str
    introduction: str
    improvement_points: List[ImprovementPoint]
    well_done_points: List[GoodPractice]
    conclusion: str

    def to_markdown(self) -> str:
        lines = [
            f"# {self.name}\n",
            f"\n{self.introduction}\n\n",
        ]
        for i, point in enumerate(self.improvement_points):
            lines.append(f"## Improvement Point {i + 1}\n")
            lines.append(f"\n**Problem**: {point.problem}\n")
            lines.append(f"\n**Solution**: {point.solution}\n")
        lines.append("\n")
        lines.append("## Good Practices\n")
        for i, practice in enumerate(self.well_done_points):
            lines.append(f"**{i + 1}.** {practice.description}\n\n")
        lines.append("\n")
        lines.append("## Conclusion\n")
        lines.append(f"{self.conclusion}\n")
        return "".join(lines)
