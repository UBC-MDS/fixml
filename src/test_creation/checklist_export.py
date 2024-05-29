import fire

from modules.checklist.checklist import Checklist, ChecklistFormat


def export_checklist(checklist_path: str):
    """Example calls. To be removed later.

    Example:
    python src/test_creation/modules/checklist/checklist.py ./checklist/test-dump-csv

    Note that the supplied path must be a directory containing 3 CSV files:
    1. `overview.csv`
    2. `topics.csv`
    3. `tests.csv`
    """
    __package__ = ''
    checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
    print(checklist.as_markdown())
    checklist.export_html("checklist.html", exist_ok=True)
    checklist.export_pdf("checklist.pdf", exist_ok=True)


if __name__ == "__main__":
    fire.Fire(export_checklist)
