from .checklist import ChecklistActions
from ..modules.workflow.parse import ResponseParser
from ..modules.workflow.response import EvaluationResponse


class ExportActions(object):

    def __init__(self):
        self.checklist = ChecklistActions().export

    @staticmethod
    def evaluation_report(json_response_path: str, export_path: str,
                          overwrite: bool = False) -> None:
        """Exports the evaluation report from a given JSON file containing the
        evaluation response.

        The exported format will depend on the extension name provided in
        `output_path`.
        Valid export formats are ["pdf", "html", "htm", "qmd", "md"].

        Parameters
        ----------
        json_response_path : str
            The path to the JSON file containing the evaluation response.
        export_path: str
            The path to the exported file.
        overwrite : bool, optional
            The flag to bypass overwrite protection. This is by default False.
        """
        response = EvaluationResponse.from_json(json_response_path)
        renderer = ResponseParser(response)
        renderer.export(output_path=export_path, exist_ok=overwrite)
