import os
from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

import pypandoc
import quarto

from .utils import get_extension


class WriteableMixin:
    """A mixin for classes which will write content to filesystem."""
    def _filedump_check(self, output_path: str, exist_ok: bool, expects_directory_if_exists: bool = False):
        normalized_path = os.path.abspath(os.path.normpath(output_path))
        dir_path = os.path.dirname(normalized_path)
        if not os.access(dir_path, os.W_OK):
            raise PermissionError(f"Write permission is not granted for the output path: {dir_path}")

        if not exist_ok:
            if os.path.exists(normalized_path):
                raise FileExistsError("Output file already exists. (Have you "
                                      "provided a flag/argument for "
                                      "file overwriting?)")
        elif os.path.exists(normalized_path):
            if expects_directory_if_exists and not os.path.isdir(
                    normalized_path):
                raise NotADirectoryError("An non-directory already exists in "
                                         "the path but the write operation is"
                                         " expecting to overwrite a directory.")
            elif not expects_directory_if_exists and not os.path.isfile(
                    normalized_path):
                raise IsADirectoryError("An non-file object already exists in "
                                        "the path but the write operation is "
                                        "expecting to overwrite a file.")

            if not os.access(normalized_path, os.W_OK):
                raise PermissionError(f"Write permission is not granted for the output path: {normalized_path}")
        return True


class MarkdownExportableMixin(WriteableMixin, ABC):
    """A mixin that provides functionality to export (dump) content as markdown,
    then to convert it into HTML/PDF/Quarto documents.

    Extends WriteableMixin.

    This mixin relies on markdown representations of the object.
    The class including mixin must have `.as_markdown()` and
    `.as_quarto_markdown()` implemented.
    """

    def __init__(self):
        self.export_ext_func_map = {
            'html': self.export_html,
            'htm': self.export_html,
            'pdf': self.export_pdf,
            'qmd': self.export_quarto
        }

    def export(self, output_path: str, exist_ok: bool = False):
        to_ext = get_extension(output_path)
        if to_ext not in self.export_ext_func_map.keys():
            raise ValueError(
                f"Invalid output format(s) provided. The "
                f"acceptable formats are "
                f"{list(self.export_ext_func_map.keys())}."
            )
        self.export_ext_func_map[to_ext](output_path, exist_ok)

    @abstractmethod
    def as_markdown(self) -> str:
        pass

    @abstractmethod
    def as_quarto_markdown(self) -> str:
        pass

    @staticmethod
    def _escape_single_quotes(string: str) -> str:
        return string.replace("'", "\\'")

    def __format_check(self, output_path, format):
        formats = {
            "pdf": ["pdf"],
            "html": ["htm", "html"],
            "qmd": ["qmd"]
        }

        if get_extension(output_path) not in formats[format]:
            raise ValueError(f"Output file path `{output_path}` does not meet expectation. When specifying `{format}` to be exported, please use one of the following extensions: {str(formats[format])}.")

    def _export_check(self, output_path: str, format: str, exist_ok: bool):
        self._filedump_check(output_path, exist_ok)
        self.__format_check(output_path, format)

    def export_html(self, output_path: str, exist_ok: bool = False):
        # TODO: raise error when pandoc is not installed
        self._export_check(output_path, format="html", exist_ok=exist_ok)
        pypandoc.convert_text(self._escape_single_quotes(self.as_markdown()), 'html', format='md',
                              outputfile=output_path)

    def export_pdf(self, output_path: str, exist_ok: bool = False):
        # TODO: raise error when pandoc is not installed
        # TODO: raise error when tectonic is not installed
        self._export_check(output_path, format="pdf", exist_ok=exist_ok)
        pypandoc.convert_text(self.as_markdown(), 'pdf', format='md', outputfile=output_path,
                              extra_args=['--pdf-engine=tectonic'])

    def export_quarto(self, output_path: str, exist_ok: bool = False):
        self._export_check(output_path, format="qmd", exist_ok=exist_ok)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.as_quarto_markdown())


class RenderableMixin(WriteableMixin, ABC):
    """A mixin that provides functionality to render content using Quarto.

    Extends WriteableMixin.

    This mixin relies on Quarto documents, which will be run during the
    rendering process.

    The class including mixin must have `self._qmd_template_path` sepecified.
    """

    def __init__(self, qmd_template_path: str):
        self._qmd_template = qmd_template_path

    def render(self, to: Union[str, Path], format: str = "html"):
        quarto.render(self._qmd_template,
                      execute_params={"json_file": self._response_json})

    @abstractmethod
    def as_markdown(self) -> str:
        pass

    @abstractmethod
    def as_quarto_markdown(self) -> str:
        pass

    def __format_check(self, output_path, format):
        formats = {
            "pdf": ["pdf"],
            "html": ["htm", "html"],
            "qmd": ["qmd"]
        }

        if get_extension(output_path) not in formats[format]:
            raise ValueError(f"Output file path `{output_path}` does not meet expectation. When specifying `{format}` to be exported, please use one of the following extensions: {str(formats[format])}.")

    def _export_check(self, output_path: str, format: str, exist_ok: bool):
        self._filedump_check(output_path, exist_ok)
        self.__format_check(output_path, format)
