# test_creation

<img src="img/logo.jpg" alt="test_creation logo" width="400"/>


`test_creation` is a tool designed to improve the quality and reliability of machine learning (ML) systems through comprehensive testing. By utilizing a manually curated checklist and Large Language Models (LLM), test_creation provides test completeness evaluations, missing test recommendations, and test function specification generation for ML system source codes.

For more details, see the [Documentation](https://ubc-mds.github.io/test-creation/proposal.html).

## Installation

1. Create a conda envionment using `environment.yml` in the repo:

```bash
conda env create -f environment.yml
```

2. Activate the newly created conda environment (default name `test-creation`):
```bash
conda activate test-creation
```

3. add `.env` with API key attached:
```bash
echo "OPENAI_API_KEY=..." > .env
```

4. Enjoy!

## Usage

### code_analyzer

This is used to analyze and extract information from a downloaded repo.

There is a file containing the example calls. Run:

```console
$ python ./src/code_analyzer/example.py <path-to-your-repo>
```

If `test_creation` assists your research, please cite it as follows:
```bibtex
@inproceedings{DBLP:conf/recsys/Kula15,
  author    = {John Shiu and Orix Au Yeung and Tony Shum and Yingzi Jin},
  title     = {Checklists and LLM prompts for efficient and effective test creation in data analysis},
  year      = {2024},
  url       = {http://example.com/paper.pdf},
}

```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License
test_creation is licensed under the MIT License.

## Contributors
John Shiu
Orix Au Yeung
Tony Shum
Yingzi Jin

## Credits

`test_creation` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
