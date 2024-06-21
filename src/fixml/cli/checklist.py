from ..modules.checklist.checklist import Checklist


class ChecklistActions:

    @staticmethod
    def convert(to_path: str, checklist_path: str = None,
                overwrite: bool = False) -> None:
        """Converts the checklist between all accepted formats.

        Parameters
        ----------
        to_path : str
            The path to the converted checklist.
        checklist_path : str, optional
            The path to the checklist to be converted. If not provided, the
            default checklist will be used.
        overwrite : bool, optional
            The flag to bypass overwrite protection. This is by default False.
        """
        checklist = Checklist(checklist_path)
        checklist.write_to(to_path, exist_ok=overwrite)
        print(f"Done. Checklist saved to {to_path}.")

    @staticmethod
    def export(to_path: str, checklist_path: str = None,
               overwrite: bool = False) -> None:
        """Exports the checklist to a more human-readable report format.

        The exported format will depend on the extension name provided in
        `to_path`. Valid export formats are ["pdf", "html", "htm", "qmd", "md"].

        The exported checklist cannot be read back by the system.
        If you need it to be converted into format that can be read back,
        please use the command `checklist convert` instead.

        Parameters
        ----------
        to_path : str
            The path to the converted checklist.
        checklist_path : str, optional
            The path to the checklist to be converted. If not provided, the
            default checklist will be used.
        overwrite : bool, optional
            The flag to bypass overwrite protection. This is by default False.
        """
        checklist = Checklist(checklist_path)
        checklist.export(to_path, exist_ok=overwrite)
        print(f"Done. Checklist saved to {to_path}.")

