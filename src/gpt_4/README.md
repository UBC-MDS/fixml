# How to analyze test functions from GitHub projects?

## Prerequisite

1. Locate the test functions in the repository, there are couple of ways to do that:

```
grep " test_" */*
```

or (for `unittest`):

```
grep "import unittest" */*
```

[](../../img/grep_example.png)

2. Go to the directory containing the test functions, zip all file under it:

```
zip -r ../tests.zip *
```

## ChatGPT 4.0 Prompts for Analysis

### 1. Unzip and simple analysis

Upload the `tests.zip`

```
Can you unzip the file and analyze the test functions inside?
```

[](../../img/gpt4_example.png)

### 2. Classify into Data Pipeline and ML Pipeline

```
Can you classify the tests into data pipeline related and ML pipeline related?
```

### 3. Compare ML Pipeline Between 2 Projects

Repeat the step 1 and 2 for another project

```
What do the 1st and 2nd project have in common in the ML pipeline related tests?
```

```
Can you make a table to list the mapping of the ML pipeline related tests between the 1st and the 2nd project?
```

[](../../img/compare_table_example.png)
