from ..modules.workflow.render import EvalReportRenderer


class RenderActions(object):

    @staticmethod
    def evaluation_report(eval_response_path: str, output_path: str,
                          format: str = 'html') -> None:
        """Renders the evaluation report from a given JSON file containing the
        evaluation response. This relies on Quarto installed in your system.

        Parameters
        ----------
        eval_response_path : str
            The path to the JSON file containing the evaluation response.
        output_path: str
            The path to the output HTML file.
        format
            Optional. If provided, the system will render the report in
            specified format. The format specified must be supported by Quarto.
            Default format is HTML.
        """
        renderer = EvalReportRenderer(eval_response_path)
        renderer.render(output_path=output_path, format=format)
