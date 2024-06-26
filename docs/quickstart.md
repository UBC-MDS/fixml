# Quickstart and Usages

Once FixML is installed, the tool offers a Command Line Interface (CLI)
command `fixml`. By using this command you will be able to evaluate your project
code bases, generate test function specifications, and perform various relevant
tasks.

```{warning}
By default, this tool uses OpenAI's `gpt3.5-turbo` for evaluation. To run any
command that requires calls to LLM (i.e. `fixml evaluate`, `fixml generate`),
an environment variable `OPENAI_API_KEY` needs to be set.

Visit [installation guide](installation.md) for more information.
```

```{note}
Currently, only calls to OpenAI endpoints are supported. This tool is still in
ongoing development and integrations with other service providers and locally
hosted LLMs are planned.
```

## Available CLI commands

Main commands:
- `fixml evaluate` - Test Evaluator
- `fixml generate` - Test Spec Generator

There are commands grouped together in the following command groups:
- `fixml export` - Report-exporting related commands
- `fixml checklist` - Checklist related commands
- `fixml repository` - Repository related commands

```{note}
Run `fixml --help` and `fixml {export|checklist|repository} --help` for more
details.
``` 


## `fixml evaluate` - Test Evaluator

The test evaluator command is used to evaluate the tests of your repository. It
generates an evaluation report and provides various options for customization,
such as specifying a checklist file, output format, and verbosity.

Here is a very basic call:
```bash
fixml evaluate /path/to/your/repo
```

This will generate a JSON file in your current working directory containing the 


Of course, a JSON file is rarely enough. `fixml evaluate` is actually very
versatile and support many options/flags to modify its behaviour. Here is an
elaborated example displaying what this command can do:
```bash
# Evaluates the repo, generate a JSON, export report after evaluation as HTML, 
# display verbose messages while performing the evaluation, overwrite existing 
# reports, use custom checklist instead of the default one, and to use GPT-4o
# instead of GPT-3.5-turbo.
  
fixml evaluate /path/to/your/repo \
  --export_report_to=./eval_report.html \
  --verbose --overwrite --model=gpt-4o \
  --checklist_path=checklist/checklist.csv
```

```{note}
The command `fixml evaluate --help` provides a comphrensive explanation on all
flags and options available.
```

## `fixml generate` - Test Spec Generator


The test spec generator command is used to generate a test specification from a
checklist. It allows for the inclusion of an optional checklist file to guide
the test specification generation process.

Example calls:
```bash
# Generate test function specifications and to write them into a .py file
# Perform the above, but to use a custom checklist
fixml generate test.py -c checklist/checklist.csv
```

```{note}
The command `fixml generate --help` provides a comphrensive explanation on all
flags and options available.
```
