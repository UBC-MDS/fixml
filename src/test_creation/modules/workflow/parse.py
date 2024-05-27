import pandas as pd
import os
from typing import Union

from ..mixins import ExportableMixin


class ResponseParser(ExportableMixin):
    def __init__(self, response):
        self.response = response
        self.evaluation_report = None

    def get_completeness_score(self, score_format: str = 'fraction', verbose: bool = False) -> Union[float, str]:
        """
        Compute Evaluation Report and Completeness Score
        """
        report_df = pd.DataFrame(self.response)['report'].explode('report').apply(pd.Series)
        report_df = report_df.rename(columns={"file": "File Path"})
        report_df['Function References'] = report_df[['File Path', 'Functions']].to_dict(orient='records')
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

        if score_format == 'fraction':
            score = f"{report_df['is_Satisfied'].sum()}/{report_df['is_Satisfied'].count()}"
        elif score_format == 'number':
            score = report_df['is_Satisfied'].sum()/report_df['is_Satisfied'].count()

        if verbose:
            print("Report:")
            print(report_df[['is_Satisfied', 'n_files_tested']])
            print()
            print(f'Score: {score}')
            print()
        return score

    def as_markdown(self) -> str:
        def _get_md_representation(content: dict, curr_level: int):
            repeated_col = [k for k, v in content.items() if isinstance(v, list)]

            # print out header for each item
            md_repr = '#' * curr_level
            if 'ID' in content.keys():
                md_repr += f" {content['ID']}"
            if 'Title' in content.keys():
                md_repr += f" {content['Title']}\n\n"
            elif 'Topic' in content.keys():
                md_repr += f" {content['Topic']}\n\n"

            # print out non-title, non-repeated items
            for k, v in content.items():
                if k not in repeated_col and k not in ['Title', 'Topic', 'ID']:
                    md_repr += f'**{k}**: {v}\n\n'

            # handle repeated columns and references
            point_form_col = ['References', 'Function References', 'Observations']
            for k in repeated_col:
                if k not in point_form_col:
                    for item in content[k]:
                        md_repr += _get_md_representation(item, curr_level=curr_level + 1)
                else:
                    md_repr += f'**{k}:**\n\n' + '\n'.join(f'  - {item}' for item in content[k]) + '\n\n'

            return md_repr

        score = self.get_completeness_score(score_format='fraction')
        summary_df = self.evaluation_report[['ID', 'Title', 'is_Satisfied', 'n_files_tested']]
        details = self.evaluation_report[['ID', 'Title', 'Requirement', 'Observations', 'Function References']].to_dict(orient='records')

        export_content = dict()
        export_content['Title'] = 'Test Evaluation Report'
        export_content['Report Areas'] = []
        export_content['Report Areas'].append({'Title': 'Summary', 'Completeness Score': score, 'Completeness Score per Checklist Item': '\n\n' + summary_df.to_markdown(index=False)})
        export_content['Report Areas'].append({'Title': 'Details', 'Report Detail': details})

        return _get_md_representation(export_content, 1)

    def as_quarto_markdown(self) -> str:
        header = '---\ntitle: "Test Evaluation Report"\nformat:\n  html:\n  code-fold: true\n---\n\n'
        return header + self.as_markdown()

    def export_evaluation_report(self, output_path, format='html', exist_ok: bool = False):
        """
        Export the test evaluation report
        """
        if format=='html':
            self.export_html(output_path, exist_ok)
        elif format=='pdf':
            self.export_pdf(output_path, exist_ok)
        return