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

We propose to develop testing suites diagnostic tools based on Large Language Models (LLMs) and curate checklists based on ML research papers and best practices to facilitate comprehensive testing of ML systems with flexibility. Our goal is to enhance applied ML software's trustworthiness, quality, and reproducibility across both the industry and academia {cite}`kapoor2022leakage`.

## Data Science Methods

### Current Approaches

To ensure the reproducibility, trustworthiness and free-of-bias ML system, comprehensive assessment is essential. We have observed some traditional approaches in assessing the quality of ML systems, which contain different advantages and drawbacks as follows.

#### 1. Code Coverage 

Code coverage is a measure of the proportion of source code of a program executed when a particular test suite is run. It is widely used in software development domain as one of the measurements. It quantifies the test quality and is scalable given the short process time. However, it cannot provide the reasons and in which ML areas that the test suites fail under the context of ML system development.

#### 2. Manual Evaluation

Manual evaluation involves human expert review at the source code, whom can take the business logic into considerations and find vulnerabilites. Manual evaluation usually delivers comments for improvement under specific development context, and it is still one of the most reliable methods in practice. However, the time cost is large and it is not scalable due to the scarcity of time and human expert. Different human expert might put emphasis on different ML test areas instead of a comprehensive and holistic review on the ML system test suites.

### Our Approach

Our approach is to deliver an automated code review tool with the best practices of ML test suites embedded, which can be used by ML users to learn the best practices as well as to obtain a comprehensive evaluation on their ML system codes.

To come up with the best practices of ML test suites, ML research paper and online resources are our data. Under the collaboration with our partner, we have researched industrial best practices (cite: Microsoft, Jordan) and published academic literature (cite: OpenJa) and consolidated the testing strategies of ML projects into a format which is easily legible and editable by human (such as researchers, ML engineers, etc.). The format is also machine-friendly that can be easily incorporated into the automated tool.

To develop our automated code review tool, GitHub repositories of ML projects are our data. We have collected 11 repositories studied in {cite}`openja2023studying`, where these projects include comprehensive test suites and are written in Python programming language, for our product development. Our tool is capable of understanding the test suites in these projects, comparing and contrasting the test suites with the embedded best practices, and delivering evaluations and suggestions to the current test suties.

By developing our approach, we expect that it can provide reliable test suites evaluation to multiple ML projects in a scalable manner. However, we acknowledged that the consolidation of best practices currently focused on a few high priority test areas due to time constraint, where we expect to expand in the future. The test evaluation results provided by our tool are yet as reliable as human evaluation, where we will quantify its performance using the success metrics below.

### Success Metrics (FIXME: this section is to be removed?)

To properly evaluate the performance of our tool where its core part leverages the capability of LLMs, we have researched and taken reference of the study in {cite}`alexander2023evaluating` and defined the 2 success metrics: accuracy and consistency. With these metrics, our users (such as researchers, ML engineers, etc.) can assess the trustworthiness while obtaining the evaluation results from our tool.

#### 1. Accuracy of the Application Response vs Human Expert Judgement

We begin by running 30 times with our tool on the 11 ML projects in {cite}`openja2023studying` to obtain the evaluation results per each ML test best practice item (i.e. the satisfying score). We then manually assess the test suites of these ML projects based on the same best practice items as the ground truth data. Machine evaluation results are compared and contrasted with the ground truth data and are summarized into distributions of how many run results match/mismatch in general and per best practice item. Accuracy is defined as the number of matching results over total number of results.

#### 2. Consistency of the Application Response

We begin by the 30 run results as mentioned above. The standard deviation of these run results per ML projects will be calculated as a measure of consistency. These standard deviations are summarized into distributions in general and per best practice item. The distributions are studied to deduce the directions of improvement of our tool for better results.

## Data Product & Results
### Data Products

Our solution offers a Python package that facilitates the use of LLMs in
checklist-based evaluation on the robustness of users' Machine Learning
projects.

The package are made publicly available for distribution on the Python Packaging
Index (PyPI).

#### Consideration when making the product
(TODO)
- Python being the dominant language in ML/DS landscape
- Ubiquitous presence of python across OSes
- Existing libraries for integration with LLMs

#### Ways to interact with the product

There are two ways to make use of this package:

1. **As a CLI tool.** A runnable command `fixml` is provided by the package.
   Once installed, users can perform the codebase evaluation, test function
   specification generation and other relevant tasks by running subcommands
   under `fixml` in terminal environment.
2. **As a high-level API.** Alternatively, one can use the package to import
   all components necessary for performing the tasks. The workflows used in the
   package have been designed to be fully modular as we have taken an
   object-oriented approach. One can easily switch between different prompts,
   models and checklists to use. Documentations are provided in terms of 
   docstrings and a rendered ReadtheDocs site 

#### System Design

(TODO)

(To be revised)
![image](../../img/proposed_system_overview.png)

The pro...

- adhere to OO Design and SOLID principles 
- fully modular
- Promotes code reuse and invites users to extend functionality

#### System Components
(TODO)
1. Code Analyzer
    - Necessity for extracting information from code base i.e. token limit
    - RAG often omit important files & depends on quality of the query
    - ways to extract information from code base
2. Prompt Templates
    - Necessity for instructing LLM to behave as expected and return consistent
      and workable response
    - format instruction, used few-shot learning in prompt
3. Runners - Evaluator and Generator
    - current approach: per file evaluation
    - validation logics and tools used
    - record all relevant information during the run
4. Checklist
    - incorporates human expertise
    - decision for using CSV as format
    - included inside the package for distribution
    - class to read CSV as a dict with fixed schema for injection into prompt
5. Parsers
    - purpose: parsing response into reports
    - which template engine used and why
    - available formats
    - external dependencies e.g. pandoc, quarto

#### Checklist Design

One big challenge in utilizing LLMs to reliably and consistently evaluate ML
systems is their tendency to generate illogical and/or factually wrong
information known as hallucination {cite}`zhang2023sirens`.

To combat this, the system will incorporate a
checklist ([Fig. 1](overview-diagram)) which would be curated manually and
incorporate best practices in software testing and identified areas to be tested
inside ML pipeline from human experts and past research.

This checklist will be our basis in evaluating the effectiveness and
completeness of existing tests in a given codebase. Relevant information will be
injected into a prompt template, which the LLMs would then be prompted to follow
the checklist's requirements **exactly** during the evaluation.

Here is an example of how the checklist would be structured:

(TODO)

(To be revised, also need to talk about the schema of the checklist)
![image](../../img/checklist_sample.png)

#### Intermediate Artifact Design
(TODO)
- Consideration to output intermediate artifact
- why JSON
- Examples to use these JSONs in downstream tasks i.e. rendering reports, 
  comparison between runs
- schema of the JSON saved & what kind of information is stored

### Evaluation Artifacts

The end goal of our product is to generate the following three artifacts in relation to the evaluation of a given ML system codebase:

1. **ML Test Completeness Score**: The application utilizes LLMs and our curated checklist to analyze users' ML system source code and returns a comprehensive score of the system's test quality.
  
2. **Missing Test Recommendations**: The application evaluates the adequacy of existing tests for users' ML code and offers recommendations for additional, system-specific tests to enhance testing effectiveness.
  
![image](../../img/test_evaluation_report_sample.png)

3. **Test Function Specification Generation**: Users select desired test recommendations and prompt the application to generate test function specifications and references. These are reliable starting points for users to enrich the ML system test suites.

### Evaluation Results
  
We assessed the quality of evaluation determined by the system by examining the breakdown of the ML Completeness Score using the repositories mentioned in Openja et al. (2023) on two metrics: Accuracy and Consistency. (FIXME: would it be better to show a table of the repos? like how the Openja does?) We ran 30 iterations on each of the repositories.

#### Accuracy

To examine the accuracy of the output on a given repository, we need ground truth, i.e., satisfied or not satisfied for each checklist item, on that repository. We manually evaluated the lightfm (FIXME: link), qlib (FIXME: link), and DeepSpeech (FIXME: link) repositories and compared the system output to the manually created ground truth.

(FIXME: table: checklist id, title, (ground truth, (lightfm, qlib, DeepSpeech)))

The plot below shows the comparison of the satisfaction determined by our system for each checklist item and the ground truth for `lightfm`, `qlib`, and `DeepSpeech`.

(FIXME: jitter-mean-sd plot (checklist item vs. score) for each repo)

We found that for the items that are truly satisfied (score = 1), our system tends to determine them as partially satisfied (score = 0.5); for the items that are partially satisfied (score = 0.5), our system often determines them as not satisfied (score = 0). The table below summarizes our findings for each repository.

(FIXME: contingency table)

The inaccuracies may be attributed to the need for improvement in the prompt for each checklist item, defined in the "Requirement" in the checklist.

#### Consistency 

The LLM output is not deterministic, so the completeness score is also not deterministic. The question we want to examine here is: How inconsistent are the scores for the checklist items?

The chart below shows the standard deviations of the score for each checklist item, with each colored dot corresponding to the standard deviation of a checklist item from 30 runs of a specific repository.

(FIXME: jitter-boxplot, checklist item vs. SD)

We found that some items, e.g., item 3.2 "Data in the Expected Format," tend to have high standard deviations for all the repositories. This might be due to the poor quality of the prompt, making it ambiguous for the LLM and hence hard to produce consistent results. Prompt engineering might solve this problem.

On the other hand, items like 5.3 "Ensure Model Output Shape Aligns with Expectation" tend to have lower standard deviations, but there are outliers yielding exceptionally high standard deviations. This may be because those repositories are unorthodox, and careful manual examination is required to achieve a more robust conclusion.

(FIXME: where to include the comparison and comments about 3.5-turbo to 4o?)


## Conclusion

### Wrap Up

Our project, FixML, represents a significant step forward in the field of machine learning (ML) testing by providing tools that automate and enhance the evaluation and creation of test cases for ML models. The development and implementation of FixML have been driven by the need to address the limitations of traditional testing methods, which are often either too general or focus on quantitative metrics without testing the quality of ML or data science projects. FixML offers the advantages of combining the efficiency of automated testing with the thoroughness of expert evaluation, making it both scalable and reliable for diverse ML applications.

#### Key aspects of FixML

FixML seamlessly integrates with the user’s codebase, automatically analyzing the code and identifying existing test cases. This automated evaluation process leverages Large Language Models (LLMs) to assess the completeness and quality of existing tests, providing a comprehensive test completeness score. Additionally, FixML includes an automated test function specification generator that produces test function specifications based on checklist items, helping users create comprehensive test suites.

Efficiency and automation are central to FixML’s design. By automating the evaluation process, FixML significantly reduces the time and effort required to assess the quality of machine learning (ML) tests. This combination of automated testing and expert evaluation ensures thorough and efficient quality assessment.

Comprehensive reporting is another crucial aspect of FixML. The system generates detailed evaluation reports that include test completeness scores and specific recommendations for improvement. These reports provide actionable insights to enhance the quality and reliability of ML projects.

By focusing on seamless integration with codebases, automated evaluation and test generation, efficiency, flexibility, customization, and comprehensive reporting, FixML offers a robust, efficient, and customizable solution for evaluating and improving the testing quality of machine learning projects.

#### Limitation & Future Improvement

While FixML provides substantial benefits, there are limitations and areas that aim to be addressed in future development:

1. Workflow Optimization

The current test evaluator and test specification generator are separate entities. This could be improved by embedding a workflow engine that allows the system to automatically take actions based on the LLM response. For instance, if the LLM response suggests that test cases are partially satisfied or non-satisfied, the system could automatically run the test generator to produce test function skeletons and then reevaluate them until they are satisfied or some threshold is met. This would create a more cohesive and efficient workflow, reducing manual intervention and improving overall system performance.

2. Performance Optimization

Performance optimization is another critical area for future development. As FixML handles large codebases and complex evaluations, optimizing the system to handle these tasks more efficiently is essential. This includes improving the speed and accuracy of the LLM responses, reducing the time taken to analyze and generate reports, and ensuring the system can scale effectively to handle more extensive and more complex projects.

3. Specialized Checklist

The current checklist is designed to be general and may not cover all specific requirements for different ML projects. Future development will focus on creating more specialized checklists for different domains and project types, allowing for more tailored evaluations. Additionally, an interface will be provided to allow users to expand the checklists or select checklist items based on their specific needs, making the system more flexible and user-centric.

4. Enhanced Test Evaluator

The current evaluation relies on the capabilities of large language models (LLMs), which can vary in consistency and accuracy. Future improvements will enhance prompt engineering techniques and provide an interface that allows users to input their customized prompts into the system. This will improve the consistency and reliability of LLM responses. Additionally, expanding support for multiple LLMs will increase robustness and flexibility, ensuring that the system remains adaptable to advancements in LLM technology.

5. Customized Test Specification

The current generator produces general test function skeletons and does not integrate specific details for the projects. Future developments will focus on incorporating function specifications alongside checklists for more precise test generation. Additionally, integrating the project codebase as context for generating more detailed and customized test functions will make the tool more effective and aligned with the specific requirements of each project.

By addressing these limitations and focusing on these future improvements, FixML will become an even more powerful tool for ensuring the quality and robustness of machine learning and data science projects.

## Official Alpha Launch
As we move forward, we are excited to officially launch the alpha version of FixML. We invite you to test our tool, provide feedback, and collaborate with us to further refine and enhance its capabilities. Together, we can make a significant impact on the quality and reliability of machine learning projects across various domains.
