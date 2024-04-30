import os
import json
import csv

directory = '../../github-api-metadata'

output_csv = '../data/github_repos.csv'

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['html_url', 'language'])

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                home_url = data.get('html_url', 'Not available')
                language = data.get('language', 'Not available')
                writer.writerow([home_url, language])

