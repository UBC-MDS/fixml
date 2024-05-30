import os
from abc import ABC, abstractmethod

import pypandoc


class WriteableMixin:
    """A mixin for classes which will write content to filesystem."""
    def _filedump_check(self, output_path: str, exist_ok: bool, expects_directory_if_exists: bool = False):
        normalized_path = os.path.abspath(os.path.normpath(output_path))
        dir_path = os.path.dirname(normalized_path)
        print(normalized_path, dir_path)
        if not os.access(dir_path, os.W_OK):
            raise PermissionError(f"Write permission is not granted for the output path: {dir_path}")

        if not exist_ok:
            if os.path.exists(normalized_path):
                raise FileExistsError("Output file already exists. Use `exist_ok=True` to overwrite.")
        elif os.path.exists(normalized_path):
            if expects_directory_if_exists and not os.path.isdir(normalized_path):
                raise NotADirectoryError("An non-directory already exists in the path but the write operation is expecting to overwrite a directory.")
            elif not expects_directory_if_exists and not os.path.isfile(normalized_path):
                raise IsADirectoryError("An non-file object already exists in the path but the write operation is expecting to overwrite a file.")

            if not os.access(normalized_path, os.W_OK):
                raise PermissionError(f"Write permission is not granted for the output path: {normalized_path}")
        return True


class ExportableMixin(WriteableMixin, ABC):
    """A mixin that provides functionality to export (dump) content as HTML/PDF/Quarto documents.

    Extends WriteableMixin.

    Relies on markdown representations of the object.
    The class including mixin must have `.as_markdown()` and `.as_quarto_markdown()` implemented.
    """
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

        normalized_ext = output_path.split(".")[-1].lower()
        if normalized_ext not in formats[format]:
            raise ValueError(f"Output file path `{output_path}` does not meet expectation. When specifying `{format}` to be exported, please use one of the following extensions: {str(formats[format])}.")

    def _export_check(self, output_path: str, format: str, exist_ok: bool):
        self._filedump_check(output_path, exist_ok)
        self.__format_check(output_path, format)

    def export_html(self, output_path: str, exist_ok: bool = False):
        self._export_check(output_path, format="html", exist_ok=exist_ok)
        pypandoc.convert_text(self._escape_single_quotes(self.as_markdown()), 'html', format='md',
                              outputfile=output_path)

    def export_pdf(self, output_path: str, exist_ok: bool = False):
        self._export_check(output_path, format="pdf", exist_ok=exist_ok)
        self._filedump_check(output_path, exist_ok)
        pypandoc.convert_text(self.as_markdown(), 'pdf', format='md', outputfile=output_path,
                              extra_args=['--pdf-engine=tectonic'])

    def export_quarto(self, output_path: str, exist_ok: bool = False):
        self._export_check(output_path, format="qmd", exist_ok=exist_ok)
        self._filedump_check(output_path, exist_ok)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.as_quarto_markdown())
