# Test Evaluation Report - lightfm

- Repo URL: https://github.com/lyst/lightfm 

## Summary

**Completeness Score**: 5.5/7

**Completeness Score per Checklist Item**: 

|   ID | Title                                             |   is_Satisfied |   n_files_tested |
|-----:|:--------------------------------------------------|---------------:|-----------------:|
|  2.1 | Ensure Data File Loads as Expected                |            1   |                7 |
|  3.2 | Data in the Expected Format                       |            1   |                7 |
|  3.5 | Check for Duplicate Records in Data               |            0   |                7 |
|  4.2 | Verify Data Split Proportion                      |            1   |                7 |
|  5.3 | Ensure Model Output Shape Aligns with Expectation |            0.5   |                7 |
|  6.1 | Verify Evaluation Metrics Implementation          |            1   |                7 |
|  6.2 | Evaluate Model's Performance Against Thresholds   |            1   |                7 |

## Details

### 2.1 Ensure Data File Loads as Expected

**Requirement**: Ensure that data-loading functions correctly load files when they exist and match the expected format, handle non-existent files appropriately, and return the expected results.

**Observations:**

  - (test_fast_functions.py) The code does not directly address data file loading.
  - (test_movielens.py) The code does not directly address data file loading.
  - (test_datasets.py) The provided code does not directly address data file loading. (But it called the data fetch function (e.g. `fetch_movielens`).)
  - (test_cross_validation.py) The provided test code does not directly address data file loading.
  - (test_evaluation.py) The code does not directly address data file loading.
  - (test_data.py) The provided code does not directly address data file loading.
  - (test_api.py) The code does not directly address data file loading.

**Function References:**

  - (test_datasets.py): 'Functions': [`test_basic_fetching_movielens`, `test_basic_fetching_stackexchange`]

### 3.2 Data in the Expected Format

**Requirement**: Verify that the data to be ingested matches the format expected by processing algorithms (like pd.DataFrame for CSVs or np.array for images) and adheres to the expected schema.

**Observations:**

  - (test_fast_functions.py) The code does not verify the format of the data to be ingested.
  - (test_movielens.py) The code does not verify the format of the data to be ingested.
  - (test_datasets.py)  The provided code ensures that the Dataset object fits users and items as expected, and verifies the shapes of interactions and feature matrices. (e.g. assert the data type (e.g. `isinstance(train, sp.coo_matrix)`))
  - (test_cross_validation.py) The code does not verify the format of the data to be ingested.
  - (test_evaluation.py) The code does not directly verify the format of the data to be ingested.
  - (test_data.py) The provided code ensures that the data (users and items) is in the expected format for the Dataset object.
  - (test_api.py) The code does not verify the format of the data to be ingested.

**Function References:**

  - (test_datasets.py): 'Functions': [`test_basic_fetching_movielens`, `test_basic_fetching_stackexchange`]
  - (test_data.py): 'Functions': [`test_fitting`, `test_fitting_no_identity`, `test_build_features`]

### 3.5 Check for Duplicate Records in Data

**Requirement**: Check for duplicate records in the dataset and ensure that there are none.

**Observations:**

  - (test_fast_functions.py) No check for duplicate records in the dataset is performed in the provided code.
  - (test_movielens.py) The code does not explicitly check for duplicate records.
  - (test_datasets.py) The code does not explicitly check for duplicate records.
  - (test_cross_validation.py)The code does not check for duplicate records.
  - (test_evaluation.py) The code does not check for duplicate records in the dataset.
  - (test_data.py) The code does not explicitly check for duplicate records.
  - (test_api.py) The code does not explicitly check for duplicate records in the dataset.

**Function References:**

### 4.2 Verify Data Split Proportion

**Requirement**: Check that the data is split into training and testing sets in the expected proportion.

**Observations:**

  - (test_fast_functions.py) The code does not involve data splitting or verification of split proportions.
  - (test_movielens.py) The code does not involve data splitting or verification of split proportions.
  - (test_datasets.py) The code does not involve data splitting or verification of split proportions.
  - (test_cross_validation.py) The code verifies the split proportion using test.nnz / float(data.nnz) == test_percentage.
  - (test_evaluation.py) The code generates data for training and testing sets but does not explicitly verify the split proportion.
  - (test_data.py) The code does not involve data splitting or verification of split proportions.
  - (test_api.py) The code does not involve data splitting for training and testing.

**Function References:**

  - (test_cross_validation.py): 'Functions': [`test_random_train_test_split`]

### 5.3 Ensure Model Output Shape Aligns with Expectation

**Requirement**: Ensure the shape of the model's output aligns with the expected structure based on the task, such as matching the number of labels in a classification task.

**Observations:**

  - (test_fast_functions.py) The code does not relate to model output shape alignment.
  - (test_movielens.py) The code does not address model output shape alignment.
  - (test_datasets.py) The code does not relate to model output shape alignment.
  - (test_cross_validation.py) The code does not relate to model output shape alignment.
  - (test_evaluation.py) The code does not address model output shape alignment.
  - (test_data.py) The code does not relate to model output shape alignment.
  - (test_api.py) The code includes model prediction and rank computation and verifies the output values. But there is no assertion/other method to verify model output shape alignment.

**Function References:**

  - (test_api.py): 'Functions': [`test_predict`, `test_predict_ranks`]

### 6.1 Verify Evaluation Metrics Implementation

**Requirement**: Verify that the evaluation metrics are correctly implemented and appropriate for the model's task.

**Observations:**

  - (test_fast_functions.py) The code does not verify evaluation metrics implementation.
  - (test_movielens.py) The code implements evaluation metrics such as precision_at_k and auc_score. But there is no assertion/other method to verify the calculation.
  - (test_datasets.py) The code does not verify evaluation metrics implementation.
  - (test_cross_validation.py) The code does not directly verify evaluation metrics implementation.
  - (test_evaluation.py) Precision, recall, and AUC are common evaluation metrics for classification task. Test functions computes the evaluation metrics using `_precision_at_k`, `_recall_at_k`, `_auc` and compare the results from package `evaluation` to ensure the metrics in the package are correctly computed, e.g. 
    ```
        precision = evaluation.precision_at_k(model, test, k=k)
        expected_mean_precision = _precision_at_k(model, test, k)
        assert np.allclose(precision.mean(), expected_mean_precision)
    ```
  - (test_data.py) The code does not verify evaluation metrics implementation.
  - (test_api.py) The code does not verify evaluation metrics implementation.

**Function References:**

  - (test_movielens.py): 'Functions': [`_get_metrics`]
  - (test_evaluation.py): 'Functions': [`test_precision_at_k`,`test_recall_at_k`,`test_auc_score`]

### 6.2 Evaluate Model's Performance Against Thresholds

**Requirement**: Compute evaluation metrics for both the training and testing datasets and ensure that these metrics exceed predefined threshold values, indicating acceptable model performance.

**Observations:**

  - (test_fast_functions.py) The code does not evaluate the model's performance against thresholds.
  - (test_movielens.py) Most test functions evaluates model performance against predefined threshold values for metrics like precision and AUC, e.g. 
  ```
    assert roc_auc_score(train.data, train_predictions) > 0.84
    assert roc_auc_score(test.data, test_predictions) > 0.76
  ```
  - (test_datasets.py) The code does not evaluate the model's performance against thresholds.
  - (test_cross_validation.py) The code does not evaluate the model's performance against thresholds.
  - (test_evaluation.py) The code includes tests for precision, recall, and AUC scores. But there is no comparison against predefined threshold values.
  - (test_data.py) The code does not evaluate the model's performance against thresholds.
  - (test_api.py) The code does not evaluate the model's performance against thresholds..

**Function References:**

  - (test_movielens.py): 'Functions': [`test_movielens_accuracy`, `test_logistic_precision`, `test_bpr_precision`, `test_bpr_precision_multithreaded`, `test_warp_precision`, `test_warp_precision_high_interaction_values`, `test_bpr_precision_high_interaction_values`, `test_warp_precision_multithreaded`, `test_warp_precision_adadelta`, `test_warp_precision_adadelta_multithreaded`, `test_warp_precision_max_sampled`, `test_warp_kos_precision`,  `test_movielens_genre_accuracy`, `test_movielens_both_accuracy`, `test_movielens_accuracy_fit`, `test_movielens_accuracy_pickle`, `test_movielens_accuracy_resume`, `test_movielens_accuracy_sample_weights_grad_accumulation`, `test_state_reset`, `test_user_supplied_features_accuracy`, `test_zeros_negative_accuracy`, `test_zero_weights_accuracy`, `test_hogwild_accuracy`, `test_movielens_excessive_regularization`, `test_overfitting`, `test_regularization`]
  - (test_evaluation.py): 'Functions': [`test_precision_at_k`, `test_precision_at_k_with_ties`, `test_recall_at_k`, `test_auc_score`, `test_intersections_check`]

## Communication Records
[#113](https://github.com/UBC-MDS/test-creation/issues/113)
