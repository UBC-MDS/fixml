from ..modules.checklist.checklist import Checklist, ChecklistFormat


class ChecklistActions(object):

    @staticmethod
    def convert(from_format, from_path, to_format, to_path, overwrite=False):
        """Converts the checklist between all accepted formats.

        Parameters
        ----------
        from_format
            The format of the checklist to be converted.
        from_path
            The path to the checklist to be converted.
        to_format
            The format of the checklist after conversion.
        to_path
            The path to the converted checklist.
        overwrite
            The flag to bypass overwrite protection. This is by default False.

        Returns
        -------

        """
        from_format = from_format.lower()
        to_format = to_format.lower()
        format_maps = {
            'csv': ChecklistFormat.CSV,
            'yaml': ChecklistFormat.YAML
        }
        if (from_format not in format_maps.keys() or to_format not in
                format_maps.keys()):
            raise ValueError(f"Invalid format(s) provided. The acceptable "
                             f"formats are {list(format_maps.keys())}.")
        checklist = Checklist(from_path, format_maps[from_format])
        if to_format == "yaml":
            checklist.to_yaml(to_path, no_preserve_format=True,
                              exist_ok=overwrite)
        elif to_format == "csv":
            checklist.to_csv(to_path, exist_ok=overwrite)
        print(f"Done. Checklist saved to {to_path}.")

    @staticmethod
    def export(from_format, from_path, to_format, to_path, overwrite=False):
        """Exports the checklist to a more human-readable report format.

        The exported checklist cannot be read back by the system.
        If you need it to be converted into format that can be read back,
        please use the command `checklist convert` instead.

        Parameters
        ----------
        from_format
            The format of the checklist to be converted.
        from_path
            The path to the checklist to be converted.
        to_format
            The format of the checklist after conversion.
        to_path
            The path to the converted checklist.
        overwrite
            The flag to bypass overwrite protection. This is by default False.

        Returns
        -------

        Examples
        --------
        >>> test-creation checklist export csv ./checklist/checklist_demo.csv html ./report/checklist_report.html --overwrite

        """

