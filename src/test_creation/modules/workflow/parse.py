import pandas as pd


class ResponseParser:
    def __init__(self, response):
        self.response = response

    def get_completeness_score(self) -> str:
        report_df = pd.DataFrame(self.response)['report'].explode('report').apply(pd.Series)
        report_df = report_df.groupby(['ID', 'Title']).agg({
            'Score': ['max', 'count'],
            'Functions': ['sum']
        })
        report_df.columns = ['is_Satisfied', 'n_files_tested', 'functions']
        score = f"{report_df['is_Satisfied'].sum()}/{report_df['is_Satisfied'].count()}"
        print("Report:")
        print(report_df)
        print()
        print(f'Score: {score}')
        print()
        return score
