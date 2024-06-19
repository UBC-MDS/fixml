# Final Report - Checklists and LLM prompts for efficient and effective test creation in data analysis

by John Shiu, Orix Au Yeung, Tony Shum, Yingzi Jin

## Executive Summary

TBC

## Introduction

### Problem Statement

The global artificial intelligence (AI) market is growing exponentially {cite}`grand2021artificial`, driven by its ability to autonomously make complex decisions impacting various aspects of human life, including financial transactions, autonomous transportation, and medical diagnosis. 

However, ensuring the software quality of these systems remains a significant challenge {cite}`openja2023studying`. Specifically, the lack of a standardized and comprehensive approach to testing machine learning (ML) systems introduces potential risks to stakeholders. For example, inadequate quality assurance in ML systems can lead to severe consequences, such as substantial financial losses ({cite}`Asheeta2019`, {cite}`Asheeta2019`, {cite}`Asheeta2019`) and safety hazards. 

Therefore, defining and promoting an industry standard and establishing robust testing methodologies for these systems is crucial. But how?

### Our Objectives

We propose to develop testing suites diagnostic tools based on Large Language Models (LLMs) and curate a checklist to facilitate comprehensive testing of ML systems with flexibility. Our goal is to enhance applied ML software's trustworthiness, quality, and reproducibility across both the industry and academia {cite}`kapoor2022leakage`.

## Data Science Methods

### Other Approaches

### Our Approach

### Data
#### 1) ML Research Paper & Resources 

#### 2) GitHub Repositories
In this project, GitHub repositories are our data. 

To develop our testing checklist, we will collect 11 repositories studied in {cite}`openja2023studying`. Additionally, we will collect 377 repositories identified in the study by {cite}`wattanakriengkrai2022github` for our product development.

For each repository, we are interested in the metadata and the ML modeling- and test-related source code. The metadata will be retrieved using the GitHub API, while the source code will be downloaded and filtered using our custom scripts. To ensure the relevance of the repositories to our study, we will apply the following criteria for filtering:
 1. Repositories that are related to ML systems.
 2. Repositories that include test cases.
 3. Repositories whose development is written in the Python programming language.

### Success Metrics (FIXME: this section is to be removed?)

1) Accuracy and Consistency of the Application Response vs Human Expert Judgement

{accuracy graph}

2) Our product's success will depend on mutation testing of the test functions developed based on our application-generated specifications. The evaluation metric is the success rate of detecting the perturbations introduced to the ML project code.

Our partners and stakeholders expect a significant improvement in the testing suites of their ML systems post-application usage. As a result, the testing suites will demonstrate high accuracy in detecting faults, ensuring consistency and high quality of ML projects during updates.

Our data science methodology incorporates human expert evaluation and prompt engineering to assess and enhance the test quality of ML systems.

- Human Expert Evaluation

    We will begin by formulating a comprehensive checklist for evaluating the data and ML pipeline based on the established testing strategies outlined in {cite}`openja2023studying` as the foundational framework. Based on the formulated checklist, our team will manually assess the test quality within each repository data. We will refine the checklist to ensure applicability and robustness when testing general ML systems.

- Prompt Engineering

    We will engineer the prompts for LLM to incorporate with the ML system code and the curated checklist and to serve various purposes across the three-stage process:
  
    1. Prompts to examine test cases within the ML system source codes and deliver test completeness scores.
    2. Prompts to compare and contrast the existing tests and the checklist and deliver recommendations.
    3. Prompts to generate system-specific test specifications based on user-selected testing recommendations {cite}`schafer2023empirical`


## Data Product & Results
### Data Products
Our solution offers an end-to-end application for evaluating and enhancing the robustness of users' ML systems.

![image](../../img/proposed_system_overview.png)

One big challenge in utilizing LLMs to reliably and consistently evaluate ML systems is their tendency to generate illogical and/or factually wrong information known as hallucination {cite}`zhang2023sirens`.

To combat this, the system will incorporate a checklist ([Fig. 1](overview-diagram)) which would be curated manually and incorporate best practices in software testing and identified areas to be tested inside ML pipeline from human experts and past research.

This checklist will be our basis in evaluating the effectiveness and completeness of existing tests in a given codebase. Relevant information will be injected into a prompt template, which the LLMs would then be prompted to follow the checklist **exactly** during the evaluation.

Here is an example of how the checklist would be structured:

![image](../../img/checklist_sample.png)

### Evaluation Artifacts

The end goal of our product is to generate the following three artifacts in relation to the evaluation of a given ML system codebase:

1. **ML Test Completeness Score**: The application utilizes LLMs and our curated checklist to analyze users' ML system source code and returns a comprehensive score of the system's test quality.
  
2. **Missing Test Recommendations**: The application evaluates the adequacy of existing tests for users' ML code and offers recommendations for additional, system-specific tests to enhance testing effectiveness.
  
![image](../../img/test_evaluation_report_sample.png)

3. **Test Function Specification Generation**: Users select desired test recommendations and prompt the application to generate test function specifications and references. These are reliable starting points for users to enrich the ML system test suites.

### Evaluation Results
  
We evaluated the quality of the ML Test Completeness Score and its breakdown using the repositories mentioned in Openja et al. (2023) on two metrics: Accuracy and Consistency. (FIXME: would it be better to show a table of the repos? like how the Openja does?) We run 30 runs on each of the repositories.

#### Accuracy

To examine the accuracy of the output on a given repository, we need ground truth, i.e. satisfied or not for each checklist items, on that repository. We manually evaluated the `lightfm` (FIXME: link), `qlib` (FIXME: link) and `DeepSpeech` (FIXME: link), and compared the system output to the manually created ground truth. 

(FIXME: table: checklist id, title, (ground truth, (lightfm, qlib, DeepSpeech)))

Below plot shows the comparison of the satisfaction determined by our system of each checklist and the ground truth for `lightfm`, `qlib` and `DeepSpeech`.

(FIXME: jitter-mean-sd plot (checklist item vs. score) for each repo)

We found that, for the items that are truly satisfied (score = 1), our system tends to determine them as partially satisfied (score = 0.5); for the items that are partially satisfied (score = 0.5), our system often determine them as not satisfied (score = 0). The table below summarizes our finding for each repository.

(FIXME: contingency table)

The inaccuracy may attribute to the room of improvement of the prompt of each checklist item, defined in the "Requirement" in the checklist.

#### Consistency 

The LLM output is not deterministic, so the completeness score is not deterministic too. The question we want to examine here is: How inconsistent the scores are for the checklist items?

The chart below shows the standard deviations of the score for each checklist item, and each color dot corresponds to the standard deviation of a checklist item from 30 runs of specific repository.

(FIXME: jitter-boxplot, checklist item vs. SD)

We found that some items, e.g. item 3.2 "Data in the Expected Format", tend to have high standard deviations for all the repositories. This might be due to poor quality of the prompt, in a way that the LLM finds them ambiguous and hence hard to give consistent result. Prompt engineering might solve the problem.

On the other hand, items like 5.3 "Ensure Model Output Shape Aligns with Expectation" tend to have lower standard deviations, but there are outliers yielding exceptionally high standard deviations. It may be because those repositories are unorthodox, careful manual examination is required to archive a more robust conclusion.

(FIXME: where to include the comparison and comments about 3.5-turbo to 4o?)


## Conclusion

### Wrap Up

### Limitation & Future Improvement
    - Future improvement (current feature specifc) and difficulties/limitations per product
    - Checklist
    - Test Evaluator
    - Test Spec Generator
