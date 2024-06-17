import pandas as pd
from ..workflow.parse import ResponseParser


class ConsistencyEvaluator:
    def __init__(self):
        self.evaluation_reports = None

    def evaluate(self, models, num_test_runs=2, verbose=False, version_before_refactoring=False): # FIXME: version_before_refactoring is for demo purpose, to be removed
        """
        Input the initialized TestEvaluator models, test run `num_test_runs` times to obtain the result
        models = [{'name': 'model_no1', 'model': {{model object}}}, ...]
        """
        results = []
        for item in models:
            if verbose:
                print(f'Model: {item['name']}')
                
            for test_no in range(num_test_runs):
                if verbose:
                    print(f'Test Run No.: {test_no+1}')
                
                result = dict()
                model = item['model']
                if version_before_refactoring:
                    model.evaluate()
                    report_df = pd.DataFrame(model.evaluation_result)['report'].explode('report').apply(pd.Series)
                    report_df = report_df.groupby(['ID', 'Title']).agg({
                        'Score': ['max', 'count'],
                        'Functions': ['sum']
                    })
                    report_df.columns = ['is_Satisfied', 'n_files_tested', 'functions']

                    result['report'] = report_df
                    result['score'] = model.get_completeness_score(score_format='number')
                    result['model_name'] = item['name']
                    result['test_no'] = test_no + 1
                else:
                    response = model.evaluate()
                    parser = ResponseParser(response)
                    result['score'] = parser.get_completeness_score(score_format='number')
                    result['report'] = parser.evaluation_report
                    result['model_name'] = item['name']
                    result['test_no'] = test_no+1
                results.append(result)
        self.evaluation_reports = pd.DataFrame(results)
        return

    def get_completeness_score_dist(self):
        """
        Obtain the distribution of the Test Completeness scores
        """
        completeness_score_df = self.evaluation_reports.drop(columns='report')
        completeness_score_df = completeness_score_df.pivot(index='model_name', columns='test_no', values='score')
        return completeness_score_df

    def get_consistency_dist(self):
        """
        Obtain the distribution of the consistency per checklist item
        """
        consistency_df = pd.DataFrame()
        for idx in self.evaluation_reports.index:
            result = self.evaluation_reports.iloc[idx]['report'].reset_index()
            result['test_no'] = self.evaluation_reports.iloc[idx]['test_no']
            result['model_name'] = self.evaluation_reports.iloc[idx]['model_name']
            consistency_df = pd.concat([consistency_df, result], axis = 0, ignore_index=True)
        consistency_df = consistency_df.pivot(index=['model_name', 'ID'], columns=['test_no'], values=['is_Satisfied'])
        consistency_df.columns = consistency_df.columns.droplevel(level=0)
        consistency_df['consistency'] = consistency_df.eq(consistency_df.iloc[:, 0], axis=0).all(1)
        return consistency_df
