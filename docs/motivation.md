# Motivation

## Why another tool for testing tests? Aren't code coverage tools enough?

Testing codes in Machine Learning project mostly revolves around ensuring the
findings are reproducible. To achieve this, currently it requires a lot of
manual efforts. It is because such projects usually have assumptions that are
hard to quantify in traditional software engineering approach i.e. code
coverage. One such example would be testing the model's performance, in which we
would not only to check if there is any error during training, but we also
would write tests to expect the model's performance to be consistent and
reproducible by others. Testing such codes, therefore, require us to not only
quantitatively, but also to qualitatively gauge how effective the tests are.

## OK, but we can evaluate the tests by looking into the tests by ourselves...

Yes, a common way to handle this currently is to utilize expertise from domain
experts in this area. Researches and guidelines have been done on how to
incorporate such knowledge through the use of checklists. However, this requires
manually validating the checklist items which usually results in poor
scalability and slow feedback loop for developers, which are incompatible with
today's fast-paced, competitive landscape in ML developments.

## So what does this tool offer?

This tool aims to bridge the gap between these two different approaches, by
adding Large Language Models (LLMs) into the loop, given LLMs' recent
advancement in multiple areas including NLU tasks and code-related tasks. They
have been shown to some degrees the ability to analyze codes and to produce
context-aware suggestions. This tool simplifies such workflow by providing a
command line tool as well as a high-level API for developers and researchers
alike to quickly validate if their tests satisfy common areas that are required 
for reproducibility purposes.

## LLMs are known for occasional hallucinations. How is this mitigated?

Given LLMs' tendency to provide plausible but factually incorrect information,
extensive analyses have been done on ensuring the responses are aligned with
ground truths and human expectations both accurately and consistently. Based on
these analyses, we are also able to continuously refine our prompts and
workflows.