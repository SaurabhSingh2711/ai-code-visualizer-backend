from typing import List, Dict


class AnalysisModel:
    """
    Internal model representing the complete analysis result
    of a project or codebase.
    """

    def __init__(
        self,
        files: List[dict],
        architecture: Dict,
        graph: Dict,
        diagram: Dict,
        insights: Dict
    ):
        self.files = files
        self.architecture = architecture
        self.graph = graph
        self.diagram = diagram
        self.insights = insights

    def to_dict(self) -> dict:
        return {
            "files": self.files,
            "architecture": self.architecture,
            "graph": self.graph,
            "diagram": self.diagram,
            "insights": self.insights
        }
