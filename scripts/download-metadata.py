import json
import csv
import os

import requests


DATA_PATH = "./data/raw/repo-list.csv"
API_ENDPOINT = "https://api.github.com/repos/"
STRING_TO_REMOVE = "https://github.com/"
JSON_STORE_LOCATION = "./data/processed/github-api-metadata/"
GB_TOKEN = input("Enter GitHub token:")

req_header = {
    "Authorization": "Bearer " + GB_TOKEN,
}


def main():
    with open(DATA_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [_ for _ in reader]
        repo_links = [row['Link to GitHub Repository'] for row in rows]

    repo_names = [l.replace(STRING_TO_REMOVE, '') for l in repo_links]

    if repo_names:
        os.makedirs(JSON_STORE_LOCATION, exist_ok=True)

    for name in repo_names:
        print(f"Processing {name}...", end="\r")
        link = API_ENDPOINT + name
        response = requests.get(link, headers=req_header)
        content = response.json()
        with open(JSON_STORE_LOCATION + name.replace("/", "_") + ".json", "w") as f:
            f.write(json.dumps(content))
    print("Done.")


if __name__ == "__main__":
    main()
