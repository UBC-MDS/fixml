import os
import json
import yaml
import pandas as pd
from collections import Counter

id_item_map = {
    '2.1': 'Ensure Data File Loads as Expected',
    '3.2': 'Data in the Expected Format',
    '3.5': 'Check for Duplicate Records in Data',
    '4.2': 'Verify Data Split Proportion',
    '5.3': 'Ensure Model Output Shape Aligns with Expectation',
    '6.1': 'Verify Evaluation Metrics Implementation',
    '6.2': "Evaluate Model's Performance Against Thresholds"
}

ground_truth = [
    {'repo': 'lightfm', 'id': '2.1', 'score': 1},
    {'repo': 'lightfm', 'id': '3.2', 'score': 1},
    {'repo': 'lightfm', 'id': '3.5', 'score': 0},
    {'repo': 'lightfm', 'id': '4.2', 'score': 1},
    {'repo': 'lightfm', 'id': '5.3', 'score': 0.5},
    {'repo': 'lightfm', 'id': '6.1', 'score': 1},
    {'repo': 'lightfm', 'id': '6.2', 'score': 1},
    {'repo': 'qlib', 'id': '2.1', 'score': 0.5},
    {'repo': 'qlib', 'id': '3.2', 'score': 1},
    {'repo': 'qlib', 'id': '3.5', 'score': 0},
    {'repo': 'qlib', 'id': '4.2', 'score': 0.5},
    {'repo': 'qlib', 'id': '5.3', 'score': 1},
    {'repo': 'qlib', 'id': '6.1', 'score': 1},
    {'repo': 'qlib', 'id': '6.2', 'score': 1},
    {'repo': 'DeepSpeech', 'id': '2.1', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '3.2', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '3.5', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '4.2', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '5.3', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '6.1', 'score': 0},
    {'repo': 'DeepSpeech', 'id': '6.2', 'score': 0},
]

def get_score_report_from_response(resp_path, verbose=False):
    if verbose:
        print(resp_path)
    with open(resp_path, 'rb') as file:
        response = json.load(file)
    
    reports = [] # report for each test file
    for result in response['call_results']: # one test file per response
        if result['parsed_response']:
            resp = result['parsed_response']['results']
            for item in resp:
                item['file'] = result['files_evaluated'][0] 
                item['success'] = result['success']
                reports.append(item)
        # FIXME: not handled failed run for now
        # else: # if the run is failed, the parsed_response will be None
        #     reports.append({
        #         'ID': '2.1', 
        #         'Title': '',
        #         'Requirement': '',
        #         'Observation': '',
        #         'Functions': [],
        #         'Evaluation': '',
        #         'Score': 0,
        #         'file': result['files_evaluated'][0],
        #         'success': result['success']
        #     })
    
    reports_df = pd.DataFrame(reports)
    df = (
        reports_df
        .pivot(index='file', columns='ID', values='Score')
        .rename_axis(None, axis=1)
    )
    df['success'] = reports_df.groupby(['file'])['success'].all()
    df['response_path'] = os.path.abspath(resp_path)
    
    return df.reset_index()

def get_scores_by_repo_by_run_by_file(batch_run_dir_path, record_yml='record_combine.yml', verbose=False):
    ''' Get score for each checklist item, by repository, by run and by test file
    '''
    with open(os.path.join(batch_run_dir_path, record_yml), 'r') as file:
        config = pd.DataFrame(yaml.safe_load(file))

    config['response_path'] = config['response_path'].apply(
        lambda x: os.path.abspath(os.path.join(batch_run_dir_path, x))
    )
    
    tmp = [
        get_score_report_from_response(
            os.path.join(batch_run_dir_path, path),
            verbose=verbose
        ) for path in config['response_path']
    ]
    tmp = pd.concat(tmp, axis=0).reset_index(drop=True)
    
    return config.merge(tmp, on='response_path', how='left')

def preprocess(df_repo_run_file, id_item_map=None):
    if id_item_map is None:
        id_item_map = {
            '2.1': 'Ensure Data File Loads as Expected',
            '3.2': 'Data in the Expected Format',
            '3.5': 'Check for Duplicate Records in Data',
            '4.2': 'Verify Data Split Proportion',
            '5.3': 'Ensure Model Output Shape Aligns with Expectation',
            '6.1': 'Verify Evaluation Metrics Implementation',
            '6.2': "Evaluate Model's Performance Against Thresholds"
        }

    # prepare score data by repo, by run
    df_repo_run = df_repo_run_file.groupby(['repo', 'run']).agg({
        id: ['max'] for id in id_item_map.keys()
    })
    df_repo_run.columns = [col[0] for col in df_repo_run.columns]
    df_repo_run = df_repo_run.reset_index()
    
    # prepare statistics of scores by repo
    df_repo__stat = df_repo_run.groupby(['repo']).agg({
        id: ['mean', 'std', 'count'] for id in id_item_map.keys()
    })
    df_repo__stat = pd.melt(df_repo__stat.reset_index(), id_vars=[('repo', '')])
    df_repo__stat.columns = ['repo', 'id', 'stat', 'value']
    df_repo__stat = (
        df_repo__stat.pivot(index=['repo', 'id'], columns='stat', values='value')
        .reset_index()
        .rename_axis(None, axis=1)
    )
    df_repo__stat['title'] = df_repo__stat['id'].apply(lambda x: id_item_map[x])
    df_repo__stat['id_title'] = df_repo__stat['id'] + '. ' + df_repo__stat['title']
    
    # prepare counting of scores by repo
    df_repo__count = df_repo_run.groupby(['repo'])['2.1'].apply(Counter).reset_index()
    for id in list(id_item_map.keys())[1:]:
        df_repo__count = df_repo__count.merge(
            df_repo_run.groupby(['repo'])[id].apply(Counter).reset_index(),
            on=['repo', 'level_1'],
            how='outer'
        )
    #df_repo__count['title'] = df_repo__count['id'].apply(lambda x: id_item_map[x])
    
    df_repo__count = df_repo__count.fillna(0)

    df_repo_run = df_repo_run.melt(id_vars=['repo', 'run'], var_name='id', value_name='score')
    df_repo_run['title'] = df_repo_run['id'].apply(lambda x: id_item_map[x])
    df_repo_run['id_title'] = df_repo_run['id'] + '. ' + df_repo_run['title']
    
    return (df_repo_run, df_repo__stat, df_repo__count)


for model in ['3.5-turbo', '4-turbo', '4o']:
    df_repo_run_file = get_scores_by_repo_by_run_by_file(f'data/batch_run/batch_run_{model}/')
    df_repo_run, df_repo__stat, df_repo__count = preprocess(df_repo_run_file)

    df_repo_run.to_csv(f'data/processed/score_by_repo_run_{model}.csv', index=False)
    df_repo__stat.to_csv(f'data/processed/score_stat_by_repo_{model}.csv', index=False)
    df_repo__count.to_csv(f'data/processed/score_count_by_repo_{model}.csv', index=False)

ground_truth_df = pd.DataFrame(ground_truth)
ground_truth_df['title'] = ground_truth_df['id'].apply(lambda x: id_item_map[x])
ground_truth_df = ground_truth_df.pivot(index=['id', 'title'], columns='repo', values='score')
ground_truth_df.to_csv('data/processed/ground_truth.csv')