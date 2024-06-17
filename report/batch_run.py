import fire
import os
import yaml

from tqdm import tqdm
from test_creation.cli.repository import RepositoryActions

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    def main(config_yml):
        """
        Example
        ----------
        >>> python ./batch_run.py --config_yml='./batch_run.yml'
        """
        action = RepositoryActions()

        with open(config_yml, 'r') as file:
            config = yaml.safe_load(file)

        runs = config['runs']
        checklist_path = config['checklist_path']
        from_dir = config['repo_base_path']
        to_dir = config['response_path']
        repos = config['repo']

        record = []
        for repo in tqdm(repos):
            for run in range(1, runs+1):
                action.evaluate(
                    repo_path=os.path.join(from_dir, repo['path']),
                    save_to=f"{to_dir}/{repo['name']}_{"{:02d}".format(run)}.json",
                    checklist_path=checklist_path
                )
                
                record.append({
                    'repo': repo['name'],
                    'response_path': f"{to_dir}/{repo['name']}_{"{:02d}".format(run)}.json",
                    'run': run
                })
                with open(f"{to_dir}/record.yml", 'w') as file:
                    yaml.dump(record, file)

    fire.Fire(main)