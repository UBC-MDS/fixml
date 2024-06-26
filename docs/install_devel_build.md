# Install Development Build

If you are interested in helping the development of this tool, or you would like
to get the cutting-edge version of this tool, you can install this tool via
conda.

To do this, ensure you have Miniconda/Anaconda installed on your system. You can
download miniconda
on [their official website](https://docs.anaconda.com/miniconda/).


1. Clone this repository from GitHub:
   ```bash
   git clone git@github.com:UBC-MDS/fixml.git
   ```

2. Create a conda environment:

    ```bash
    cd fixml && conda env create -f environment.yml
    ```

3. Activate the newly created conda environment (default name `fixml`):

    ```bash
    conda activate fixml
    ```

4. Use `poetry` which is preinstalled in the conda environment to create a local
   package install:

    ```bash
    poetry install
    ```

5. Done! You should now be able to run unit tests to confirm the build works 
   without problems:
    ```bash
    # skip integration tests
    pytest -m "not integeration"

    # run ALL tests, which requires OPENAI_API_KEY to be set
    echo "OPENAI_API_KEY={your-openai-api-key}" > .env
    pytest
    ```
   
```{note}
For a more detailed walkthrough on how to set up the OpenAI API key , please
refer to the
[API key section of our installation guide](installation.md#configuring-api-keys).
```