from ..modules.checklist.checklist import Checklist


class ChecklistActions(object):

    @staticmethod
    def convert(from_path: str, to_path: str, overwrite: bool = False) -> None:
        """Converts the checklist between all accepted formats.

        Parameters
        ----------
        from_path
            The path to the checklist to be converted.
        to_path
            The path to the converted checklist.
        overwrite
            The flag to bypass overwrite protection. This is by default False.
        """
        checklist = Checklist(from_path)
        checklist.write_to(to_path, exist_ok=overwrite)
        print(f"Done. Checklist saved to {to_path}.")

    @staticmethod
    def export(from_path: str, to_path: str, overwrite: bool = False) -> None:
        """Exports the checklist to a more human-readable report format.

        The exported checklist cannot be read back by the system.
        If you need it to be converted into format that can be read back,
        please use the command `checklist convert` instead.

        Parameters
        ----------
        from_path
            The path to the checklist to be converted.
        to_path
            The path to the converted checklist.
        overwrite
            The flag to bypass overwrite protection. This is by default False.
        """
        checklist = Checklist(from_path)
        checklist.export(to_path, exist_ok=overwrite)
        print(f"Done. Checklist saved to {to_path}.")

