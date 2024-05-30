import fire

from test_creation.modules.checklist.checklist import Checklist, ChecklistFormat


class Converter():
    """Simple converter for converting YAML/CSV checklists."""
    def __init__(self, overwrite=False):
        self.overwrite = overwrite

    def yaml_to_csv(self, input_path, output_path):
        """Converts Checklist from YAML format to CSV."""
        checklist = Checklist(input_path, ChecklistFormat.YAML)
        checklist.to_csv(output_path, exist_ok=self.overwrite)

    def csv_to_yaml(self, input_path, output_path):
        """Converts Checklist from CSV format to YAML."""
        checklist = Checklist(input_path, ChecklistFormat.CSV)
        checklist.to_yaml(output_path, no_preserve_format=True, exist_ok=self.overwrite)


if __name__ == '__main__':
    fire.Fire(Converter)
