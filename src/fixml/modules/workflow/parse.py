from typing import Optional, Union

import pandas as pd
import os

from ..template import TemplateLoader
from .response import EvaluationResponse
from ..mixins import ExportableMixin
from ..utils import get_extension


class ResponseParser(ExportableMixin):
    def __init__(self, response: EvaluationResponse):
        super().__init__()
        self.response = response
        self.evaluation_report = None
        self.repository = self.response.repository.object
        self.git_context = self.repository.git_context
        self.items = []
        self.export_template = TemplateLoader.load("evaluation")

    def _parse_items(self):
        items = []
        for result in self.response.call_results:
            response = result.parsed_response['results']
            for item in response:
                fp = result.files_evaluated[0]
                item['File Path'] = fp
                if self.repository:
                    item['lineno'] = [self.repository.ffl_map['Python'][fp][func] for func in item['Functions']]
                else:
                    item['lineno'] = []
                item['Referenced Functions'] = [
                    f"[{func}]({self.repository.get_git_direct_link(fp, lineno)})"
                    for func, lineno in zip(item['Functions'], item['lineno'])
                ]
                items.append(item)
        self.items = items
        return items

    def get_completeness_score(self, score_format: str = 'fraction', verbose: bool = False) -> Optional[Union[float, str]]:
        """Compute Evaluation Report and Completeness Score."""

        # TODO: change this after putting the logic to load data from JSON file
        #  instead of from a Python object.
        if not self.response.call_results:
            raise NotImplementedError(
                "Response contains no results from LLM. (No files were passed?)"
                " This is a won't fix for now as the response will be written "
                "into a JSON file and to be read here later on."
            )

        for result in self.response.call_results:
            if not result.success:
                print("failed to obtain valid response, cannot calculate completeness score")
                return None

        items = self._parse_items()

        report_df = pd.DataFrame(items)
        report_df['Function References'] = report_df[['File Path', 'Referenced Functions']].to_dict(orient='records')
        report_df['Observation'] = '(' + report_df['File Path'].apply(lambda x: os.path.split(x)[-1]) + ') ' + \
                                   report_df['Observation']
        report_df = report_df.groupby(['ID', 'Title']).agg({
            'Requirement': ['max'],
            'Score': ['max', 'count'],
            'Observation': [list],
            'Function References': [list],
        })
        report_df.columns = ['Requirement', 'is_Satisfied', 'n_files_tested', 'Observations', 'Function References']
        self.evaluation_report = report_df.reset_index()

        num_items_satisfied = report_df['is_Satisfied'].sum()
        num_items = report_df['is_Satisfied'].count()
        fraction_satisfied = num_items_satisfied / num_items

        if verbose:
            print("Report:")
            n_files_tested = report_df['n_files_tested'].unique()
            if n_files_tested.shape[0] == 1:
                print(report_df[['is_Satisfied']])
                print()
                if n_files_tested[0] == 1:
                    print(f"{n_files_tested[0]} test file is tested.")
                else:
                    print(f"{n_files_tested[0]} test files are tested.")
                print()
            else:
                print(report_df[['is_Satisfied', 'n_files_tested']])
                print()
                print(f"WARNING: `n_files_tested` is not unique!")
                print()
            print(f'Result: {num_items_satisfied} items are satisfied out of {num_items}')
            print(f'Score: {fraction_satisfied:.1%}')
            print()

        if score_format == 'fraction':
            return f"{num_items_satisfied}/{num_items}"
        elif score_format == 'number':
            return fraction_satisfied

    def as_markdown(self, add_quarto_header: bool = False) -> str:

        score = self.get_completeness_score(score_format='fraction')
        summary_df = self.evaluation_report[['ID', 'Title', 'is_Satisfied', 'n_files_tested']]

        response = self.response
        call_results = response.call_results

        metadata = {
            "template_path": self.export_template.filename,
        }
        run_details = {
            "checklist_path": response.checklist.path,
            "repo_path": response.repository.path,
            "head_commit": response.repository.git_commit,
            "start_time": min([x.start_time for x in call_results]),
            "end_time": max([x.end_time for x in call_results]),
            "time_taken": max([x.end_time for x in call_results]) - min([x.start_time for x in call_results]),
            "input_token_count": sum([x.tokens_used.input_count for x in call_results]),
            "output_token_count": sum([x.tokens_used.output_count for x in call_results]),
            "successful_count": sum([x.success for x in call_results]),
            "failure_count": sum([not x.success for x in call_results]),
            "success_perc": sum([x.success for x in call_results]) / len(call_results),
            "files_evaluated": [file for x in call_results for file in x.files_evaluated],
            "model_name_used": response.model.name,
        }
        eval_summary = {
            "table": summary_df.to_markdown(index=False),
            "score": score
        }
        eval_details = self.evaluation_report[['ID', 'Title', 'Requirement', 'Observations', 'Function References']].to_dict(orient='records')

        vars = {
            "quarto_header": add_quarto_header,
            "title": "Test Evaluation Report",
            "metadata": metadata,
            "run_details": run_details,
            "eval_summary": eval_summary,
            "eval_details": eval_details
        }
        return self.export_template.render(**vars)

    def as_quarto_markdown(self) -> str:
        return self.as_markdown(add_quarto_header=True)

    def export_evaluation_report(self, output_path,
                                 exist_ok: bool = False) -> None:
        """
        Export the test evaluation report
        """
        ext = get_extension(output_path)
        self.export_ext_func_map[ext](output_path, exist_ok)
