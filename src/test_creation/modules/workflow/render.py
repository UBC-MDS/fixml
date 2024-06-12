import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from importlib.resources import files
from typing import Union
import subprocess
from shutil import move
import tempfile

import quarto

from ..mixins import WriteableMixin


class QuartoRenderer(ABC, WriteableMixin):
    def __init__(self, qmd_template_path: Union[str, Path]):
        self._qmd_template = qmd_template_path
        super().__init__()

    @abstractmethod
    def render(self, **kwargs):
        pass


class EvalReportRenderer(QuartoRenderer):
    """Object to load in evaluation response and render the data into a report
    using Quarto.

    Extends QuartoRenderer.

    This relies on Quarto documents as template, which will be run during the
    rendering process.
    """
    def __init__(self, response_json_path: Union[str, Path],
                 qmd_template_path: Union[str, Path] = None):
        self.template_file = "report.qmd"
        if not qmd_template_path:
            self.template_dir = files(
                "test_creation.data.report_templates.evaluation")
            qmd_template_path = self.template_dir / self.template_file
        super().__init__(qmd_template_path)
        self._eval_response_json_path = Path(response_json_path).resolve()

    def render(self, output_path: Union[str, Path], format: str = 'html'):
        self._filedump_check(output_path=output_path, exist_ok=True)
        path = quarto.quarto.find_quarto()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            subprocess.run(
                [path, "render", self._qmd_template, "--output-dir", tmpdir,
                 "--to", format, "-P",
                 f"json_file:{self._eval_response_json_path}"])

            # expecting output exists
            files = list(tmpdir.iterdir())
            if len(files) == 0:
                raise RuntimeError("Quarto render failed")
            elif len(files) != 1:
                raise NotImplementedError("Not implemented to handle more than 1 output files.")
            output_file = files[0]
            shutil.move(output_file, Path(output_path))
