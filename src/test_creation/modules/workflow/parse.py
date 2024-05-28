from typing import Optional

import pandas as pd

from .response import EvaluationResponse


class ResponseParser:
    def __init__(self, response: EvaluationResponse):
        self.response = response
        self.evaluation_report = None

    def get_completeness_score(self, score_format: str = 'fraction', verbose: bool = False) -> Optional[float]:
        for result in self.response.call_results:
            if not result.success:
                print("failed to obtain valid response, cannot calculate completeness score")
                return None
        parsed_responses = [result.parsed_response for result in self.response.call_results]
        report_df = pd.DataFrame(parsed_responses)['results'].explode('results').apply(pd.Series)
        report_df = report_df.groupby(['ID', 'Title']).agg({
            'Score': ['max', 'count'],
            'Functions': ['sum']
        })
        report_df.columns = ['is_Satisfied', 'n_files_tested', 'functions']
        self.evaluation_report = report_df

        if score_format == 'fraction':
            score = f"{report_df['is_Satisfied'].sum()}/{report_df['is_Satisfied'].count()}"
        elif score_format == 'number':
            score = report_df['is_Satisfied'].sum()/report_df['is_Satisfied'].count()

        if verbose:
            print("Report:")
            print(report_df)
            print()
            print(f'Score: {score}')
            print()
        return score
