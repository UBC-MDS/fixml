# Checklists and LLM prompts for efficient and effective test creation in data analysis - Initial Proposal
- Authored By John Shiu, Orix Au Yeung, Tony Shum, Yingzi Jin

# 1.0 EXECUTIVE SUMMARY

# 2.0 INTRODUCTION

## 2.1 Problem Statement
Global artificial intelligence (AI) market is growing exponentially (Ref: https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-market), which is driven by its ability to autonomously make complex decisions impacting various aspects of human life, including financial transactions, autonomous transportation, and medical diagnosis, etc. 

However, ensuring the software quality of these systems is yet an open challenge (Ref: https://arxiv.org/pdf/2312.12604). A lack of a standardized and comprehensive approach to testing machine learning (ML) systems is observed, which might pose potential risks to stakeholders. Inadequate quality assurance in ML systems could possibly link to severe consequences such as financial losses (Ref: https://www.firstpost.com/business/sebis-circular-the-black-box-conundrum-and-misrepresentation-in-ai-based-mutual-funds-6625161.html) and safety hazards, which raises our concerns about the need for robust testing methodologies.

## 2.2 Our Objectives
Quality assurance in software engineering is dependent on testing suites. Our proposal aims to enhance the trustworthiness and robustness of applied machine learning (ML) software through the development of comprehensive ML system testing suites. We seek to improve the quality and reproducibility of ML systems (Ref: https://arxiv.org/abs/2207.07048) in both industry and academia via the systematic testing approach. Ultimately, our goal is to mitigate the potential negative societal impacts associated with unreliable ML systems.

# 3.0 OUR PRODUCT
Our solution offers an end-to-end application for evaluating and enhancing the robustness of users' machine learning (ML) systems. Key features include:
1. Comprehensive Test Evaluation
2. Tailored Test Recommendations
3. Automatic Test Case Generation

## 3.1 Description
Basically, our product can be utilized into 3 stages.

- Stage 1: Comprehensive Test Evaluation

    Users input the source code of their ML systems along with our suggested prompts into the application, which utilizes Large Language Model (LLM) to identify existing test suites within the code. A comprehensive report is generated and provides qualitative (e.g., test categories/strategies covered) and quantitative (e.g., test coverage/score) evaluations of the ML system's test quality.

- Stage 2: Tailored Test Recommendations

    Based on the robust checklist created by our team for testing applied ML code, the application assesses the adequacy of existing tests. Recommendations on additional test categories/strategies are provided based on the ML system's nature and test evaluation for improvement.

- Stage 3: Automatic Test Case Generation

    Users specify desired test categories/strategies and utilize our suggested LLM prompts within the application. The application autonomously engineers reproducible test data and software tests, which serve as reliable starting points for users to improve their test suites within the ML systems.

## 3.2 Success Metrics
Success metrics of our product will be dependent on 2 areas.

1. Test Coverage Enhancement:
- Evaluation Metrics: Percentage increase in test coverage across various testing categories/strategies before and after using the application.

    Our partner and stakeholders would expect to see a significant improvement in test coverage across all relevant testing categories/strategies of their ML systems post-application usage.

2. Training/Test Evaluation Performance:
- Evaluation Metrics: Accuracy, precision, recall, and F1 score for comparing generated testing strategies/test cases with human-evaluated ones or original test cases.

    Our partner and stakeholders will expect the application to demonstrate high accuracy, precision, recall, and F1 score values, which indicates accurate replication or improvement upon existing testing strategies.

## 3.3 Data Science Approach

### 3.3.1 Data 

We will collect data from the 377 GitHub repositories identified in the study by Wattanakriengkrai et al. (2022) (Ref: https://www.sciencedirect.com/science/article/pii/S0164121221002144). The data will include repository metadata and source code sourced using GitHub API and custom scripts. To ensure relevance to our study, we will apply these criteria for filtering the data: 1) projects related to ML systems; 2) projects contain test cases; 3) test cases are written in Python or C programming languages.

{screencap/copy-and-paste of the code}

### 3.3.2 Methodologies
Our data science methodology incorporates both human expert evaluation and prompt engineering to assess and enhance the test quality of ML systems.

- Human Expert Evaluation

    We will begin by formulating a comprehensive checklist for evaluating the data and ML pipeline based on established testing strategies outlined in Openja et al. (2023) (Ref: https://arxiv.org/pdf/2312.12604) as the foundational framework. for assessing test quality within selected repositories. Our team will manually evaluate the test quality within the repository data based on the formulated checklist. The checklist will be refined during the process to ensure its applicability and robustness testing general ML systems.

- Prompt Engineering

    We will engineer prompts for LLM to serve various purposes across three stages:
    1. Prompts to examine test cases within ML system source codes and deliver qualitative and quantitative test scores.
    2. Prompts incorporated with the completed checklist to suggest potential testing strategies by comparing with ML system source codes.
    3. Prompts to generate test cases based on suggested testing strategies and ML system task types (Ref: https://ieeexplore.ieee.org/abstract/document/10329992)

### 3.3.3 Iterative Development Approach
As we leverage data from selected GitHub repositories and references research on testing strategies, it's important to acknowledge that this may not include all ML systems or testing methodologies. To address these considerations, we adopt an iterative development approach by setting up an open and scalable framework for this project. Our application could then undergo continuous updates based on users' feedback and contributors' insights.

We encourage users to interpret the artifacts generated by the application with a grain of salt and recognize the evolving nature of ML system testing practices.

# 4.0 DELIVERY TIMELINE
Our follows a timeline for our deliver. We also aim at close communication with our partner to align our product development with thei expectation.

| Timeline | Milestones |
|---|---|
| Week 1 (Apr 29) | Proposal of potential solution and Presentation, Scrape repository data |
| Week 2 (May 6) | Ship Initial Proposal, Ship Test Evaluation Function, Develop Pipeline Test Checklist   |
| Week 3 (May 13) | Fine-tune Test Evaluation Function, Ship Pipeline Test Checklist, Develop Test Recommendation Application |
| Week 4 (May 20) | Fine-tune Pipeline Test Checklist, Ship Test Recommendation Function, Develop Test Generation Function |
| Week 5 (May 27) | Fine-tune Test Recommendation Function, Ship Test Generation Function, Develop All-inclusive Application  |
| Week 6 (Jun 3) | Fine-tune Test Generation Function, Ship All-inclusive Application |
| Week 7 (Jun 10) | Final Product Presentation, Draft Final Product, Refine Final Product|
| Week 8 (Jun 17) | Ship Final Product, Ship Final Report |

# References
> Reference to be done with Jupyter notebook