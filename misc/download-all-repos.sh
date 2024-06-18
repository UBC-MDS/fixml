#!/usr/bin/env bash

# ==============================================================================
# download-all-repo.sh
#
# Simple Bash script to read a CSV file and download (clone) git repositories.
#
# Note: This script does not have any checking mechanisms and will assume:
# 1. The CSV file has a header (hence tail -n +2)
# 2. The repo link is at the first column of the CSV file
# 3. Errors during cloning can be omitted (e.g. repo not found, bad network)
#
# Usage:
#
# bash download-all-repo.sh path_to_csv download_path
#
# or
#
# ./download-all-repo.sh path_to_csv download_path
# ==============================================================================


if [[ -z "$2" ]]; then
  echo "Usage: download-all-repo.sh path_to_csv download_path";
  exit 1;
fi

CSV_PATH="$(pwd)/$1"
DOWNLOAD_PATH="$(pwd)/$2"

mkdir -p $DOWNLOAD_PATH && \
        cd $DOWNLOAD_PATH && \
        cut -d',' -f1 $CSV_PATH | \
        tail -n +2 | \
        while read repo_link; do git clone $repo_link; done;
        exit 0;
