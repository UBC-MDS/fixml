# Reference: 
# 	https://swcarpentry.github.io/make-novice/02-makefiles.html
# 	https://ubc-dsci.github.io/reproducible-and-trustworthy-workflows-for-data-science/materials/lectures/09-pipelines.html

# The .PHONY rule is used to tell make that 'all', 'clean' are not files.
.PHONY : all
# The 'all' target is the default target. It depends on 'report/docs/index.html', which triggers the build process for this file.
all : report/docs/index.html 

# Unzip batch_run.zip
data/batch_run/batch_run_3.5-turbo \
	data/batch_run/batch_run_4-turbo \
	data/batch_run/batch_run_4o : 
	unzip data/batch_run/batch_run.zip -d data/batch_run/

# Preprocess 
data/processed/ground_truth.csv : analysis/preprocess_batch_run_result.py data/batch_run/batch_run_3.5-turbo
	python analysis/preprocess_batch_run_result.py

# Build 'report/docs/index.html' by rendering the Jupyter notebooks using Quarto.
report/docs/index.html : data/processed/ground_truth.csv
	quarto render

# The 'clean' target is used to clean up generated files and directories.
.PHONY : clean
clean : 
	rm -rf report/docs/
	rm -rf data/batch_run/batch_run_3.5-turbo
	rm -rf data/batch_run/batch_run_4-turbo
	rm -rf data/batch_run/batch_run_4o
	rm -rf data/processed/ground_truth.csv
	rm -rf data/processed/score_*csv

