# Checklists and LLM prompts for efficient and effective test creation in data analysis - Initial Proposal
- Authored By John Shiu, Orix Au Yeung, Tony Shum, Yingzi Jin

> a maximum of 1200 words (excluding appendices, figure captions, and table captions)

# 1.0 EXECUTIVE SUMMARY

# 2.0 INTRODUCTION

## 2.1 Problem Statement

> Broad introduction to the problem statement or question being addressed.
> Importance and relevance of the problem statement.

Global artificial intelligence (AI) is growing rapidly in terms of both market size and the impact to the society (Ref: https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-market), which roots from its capability to independently make complex decisions that affects human life, including financial decision, autonomous driving, and disease diagnosis, etc.

However, ensuring the software quality of these systems is yet an open challenge (Ref: https://arxiv.org/pdf/2312.12604) and there lacks a well-recognized systematic approach of testing the machine learning (ML) systems. Our team can foresee that ML systems without sufficient quality assurance could put stakeholders at great risk, e.g. financial losses (Ref: https://www.firstpost.com/business/sebis-circular-the-black-box-conundrum-and-misrepresentation-in-ai-based-mutual-funds-6625161.html) or casualties.

## 2.2 Our Objectives

> Refinement of the problem into specific, actionable objectives.

Our team aim at making applied machine learning software more trustworthy by increasing its robustness (Ref: Dr. Timbers paper) via offering a systemic testing approach. We hope this can influence industrial and academic practices in high quality, reproducible (Ref: https://arxiv.org/abs/2207.07048) ML systems development that mitigates the risk of potential negative impact to the society.


## 2.3 Product Proposition

> What is the product?

We provide an end-to-end application to evaluate and enhance the robustness of users' ML systems, which includes
- Qualitative and quantitative evaluation on the test coverage of users' ML systems source code
- Tailored recommendations on further test coverage on users' ML systems
- Automatic test case generation based on the recommendation to enhance the trustworthiness of users' ML systems

# 3.0 OUR PRODUCT

## 3.1 Description

> Description of the final data product to be delivered to the partner.
> Example components of the data product

We provide a LLM-incorporated application, in the hope of comprehensively evaluating the test quality of applied ML software and enhancing the quality with suggested test cases.
Basically, our product can be utilized into 3 stages.

- Stage 1: Test Evaluation

    Users can insert the source code of their ML system source code and our suggested LLM prompts in the application, which will identify the test suites in the code. In return, the application generates a comprehensive report on the ML system's test quality in qualitative measures (e.g. test category/strategy covered) and quantitative measures (e.g. test coverage/score)

- Stage 2: Test Recommendation

    Based on the general and robust checklist our team created for testing applied ML code, the application can evaluate the adequacy of tests according to the nature of the ML system and the current test coverage. The application will further suggests the test categories/strategies that users can incorporate into their ML system.

- Stage 3: Test Generation

    Users can input the desired test categories/strategies and our suggested LLM prompts, which the application will engineer reproducible test data and software tests itself. The suggested tests can act as a reliable starting points for users to improve their test suites in the code.

## 3.2 Success Metrics

> which evaluation metrics you are going to use and why, as well as an explicit mention of what the partner is expecting and how you will know when you have met this expectation.
> Mention different stakeholders that will be affected by the model and why your metrics are important for them.

The test coverage in term of testing category/strategy will be the evaluation metrics. By delivering an increase in test coverage with stated details after using our application on their ML systems, our partner and users will expect a higher extent of trustworthiness of the data and/or ML pipeline within their ML systems.

For training evaluation, we will input the training data into our application and compare the generated testing strategies and/or test cases with our human-evaluated testing strategies to examine its performance.

For test evaluation, we can remove the test cases of ML systems with well-defined tests, input the source codes into our application, and compare the generated results with the original test cases.

## 3.3 Data Science Approach

> include a description of the data (variables/features and observational units) and some examples/snippets of what the data
> start with simple data science techniques to obtain a simple version of your data science product
> Discussion of potential difficulties with the data.
> Risk/Limitation of the approach/product

### 3.3.1 Data 

The data would be the repository metadata and source code of the 377 GitHub repositories as identified in Wattanakriengkrai et al. (2022) (Ref: https://www.sciencedirect.com/science/article/pii/S0164121221002144), which is sourced using GitHub API and scripts. The data is further filtered based on the criteria: 1) the projects are related to ML systems; 2) the projects contain test cases; 3) the tests are written in Python/C programming languages.

{screencap/copy-and-paste of the code}

### 3.3.2 Methodologies
The methodologies will involve both human expert evaluation and prompt engineering.

- Human Expert Evaluation

    The general and robust checklist on the data and ML pipeline will be first formulated based on the testing strategies as illustrated in Openja et al. (2023) (Ref: https://arxiv.org/pdf/2312.12604). The test quality within the selected repositories data will be evaluated and suggested test strategies will be generated by our team. The checklist will be updated simultaneously to ensure its practicality to general ML systems and robustness towards quality testing.

- Prompt Engineering

    LLM prompts will be engineered by our team that serve different purposes under 3 stages: 1) engineer prompts to examine the test cases within the ML system source codes and to deliver qualitative and quantitative test scores during our evaluation of the repositories data; 2) engineer prompts to incorporate the completed checklist and to suggest potential testing strategies via comparison with the ML system source codes; 3) engineer prompts to generate test cases based on the suggested testing strategies and ML system task type (Ref: https://ieeexplore.ieee.org/abstract/document/10329992).

### 3.3.3 Limitations
We are aware of the fact that the selected GitHub repositories data and the quoted research on testing strategies might not be representative to all ML systems or all testing strategies. It only reflects the perspectives of the authors. Regarding the limited time and resources, it is unlikely to assume that our application could cover all the tests necessary for fully testing ML systems. The application will be updated with an iterative approach and the artifacts from the application should be taken with a grain of salt by users.

# 4.0 DELIVERY TIMELINE

> Milestones to be achieved at different stages of the project.

| Timeline | Milestones |
|---|---|
| Week 1 (Apr 29) | Proposal of potential solution and Presentation |
| Week 2 (May 6) | Ship Initial Proposal, Ship Test Evaluation Function, Develop Pipeline Test Checklist   |
| Week 3 (May 13) | Fine-tune Test Evaluation Function, Ship Pipeline Test Checklist, Develop Test Recommendation Application |
| Week 4 (May 20) | Fine-tune Pipeline Test Checklist, Ship Test Recommendation Function, Develop Test Generation Function |
| Week 5 (May 27) | Fine-tune Test Recommendation Function, Ship Test Generation Function, Develop All-inclusive Application  |
| Week 6 (Jun 3) | Fine-tune Test Generation Function, Ship All-inclusive Application |
| Week 7 (Jun 10) | Final Product Presentation, Draft Final Product, Refine Final Product|
| Week 8 (Jun 17) | Ship Final Product, Ship Final Report |

# References
