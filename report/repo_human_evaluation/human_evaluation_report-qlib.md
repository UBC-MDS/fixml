# Test Evaluation Report - lightfm

- Repo URL: https://github.com/microsoft/qlib

## Summary

**Completeness Score**: 4.0/7

**Completeness Score per Checklist Item**: 

|   ID | Title                                             |   is_Satisfied |   n_files_tested |
|-----:|:--------------------------------------------------|---------------:|-----------------:|
|  2.1 | Ensure Data File Loads as Expected                |            0.5   |               31 |
|  3.2 | Data in the Expected Format                       |            1   |               31 |
|  3.5 | Check for Duplicate Records in Data |              0 |               31 |
|  4.2 | Verify Data Split Proportion                      |            0.5 |               31 |
|  5.3 | Ensure Model Output Shape Aligns with Expectation |              1 |               31 |
|  6.1 | Verify Evaluation Metrics Implementation |              1 |               31 |
|  6.2 | Evaluate Model's Performance Against Thresholds |              1 |               31 |

## Details

### 2.1 Ensure Data File Loads as Expected

**Requirement**: Ensure that data-loading functions correctly fetch datasets from predefined sources or online repositories. Additionally, verify that the functions handle errors or edge cases gracefully.

**Observations: Partially Satisfied**

  - (test_get_data.py) The script downloads data and ensures it exists (test_1_csv_data and test_0_qlib_data) (e.g. `GetData().qlib_data` and `GetData().download_data` to download a CSV file). Error handling is not explicitly shown in the provided code.
  - (test_dump_data.py) The code includes a class `TestDumpData` which uses the `GetData` class to download data and the `DumpDataAll` class to process it. However, there is no explicit error handling or edge case management observed in the provided code.
  - (test_pit.py) The code includes several functions that load data from predefined sources. The `GetData().qlib_data` function is used to fetch datasets from predefined sources. However, there is no explicit error handling or edge case management observed in the provided code.
  - (test_storage.py) `test_calendar_storage`, `test_instrument_storage`, and `test_feature_storage` test the loading of calendar, instrument, and feature data respectively. These functions also include assertions to check the data types and handle errors using `self.assertRaises` to catch `ValueError` and `IndexError` exceptions.
  - (test_handler.py) The script uses D.features to load data, demonstrating that data-loading functions work as expected. This is shown in the test_handler_df function. However, there is no explicit error handling or edge case testing observed in the provided code.
  - (test_dataset.py) The script uses TSDatasetH to load and prepare data, demonstrating that data-loading functions work as expected. This is shown in the testTSDataset function. However, there is no explicit error handling or edge case management observed in the provided code.
  - (test_processor.py) The script uses D.features to fetch data for a specific stock (TEST_INST) over a specific time period. This demonstrates that the data-loading functions work as expected. However, there is no explicit error handling or edge case management observed in the code.
  - (test_handler_storage.py) The script initializes data handlers and fetches data for specified time ranges and instruments, demonstrating that data-loading functions work as expected. This is shown in the test_handler_storage function. However, there is no explicit error handling or edge case management observed in the provided code.
  - (test_datalayer.py) The provided code includes tests that load data using the `D.features` function from the `qlib` library. However, there is no explicit error handling or edge case management in the provided code.

**Function References:**

  - {'File Path': '../../../qlib/tests/test_get_data.py', 'Functions': ['test_0_qlib_data', 'test_1_csv_data']}
  - {'File Path': '../../../qlib/tests/test_dump_data.py', 'Functions': ['setUpClass']}
  - {'File Path': '../../../qlib/tests/test_pit.py', 'Functions': ['test_query', 'test_no_exist_data', 'test_expr', 'test_unlimit', 'test_expr2', 'test_pref_operator']}
  - {'File Path': '../../../qlib/tests/storage_tests/test_storage.py', 'Functions': ['test_calendar_storage', 'test_instrument_storage', 'test_feature_storage']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_handler.py', 'Functions': ['test_handler_df']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_dataset.py', 'Functions': ['testTSDataset']}
  - {'File Path': '../../../qlib/tests/dataset_tests/test_datalayer.py', 'Functions': ['D.features']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_handler_storage.py', 'Functions': ['test_handler_storage']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_processor.py', 'Functions': ['test_MinMaxNorm', 'test_ZScoreNorm', 'test_CSZFillna', 'test_CSZScoreNorm']}

### 3.2 Data in the Expected Format

**Requirement**: Verify that the data matches the expected format. This involves checking the shape, data types, values, and any other properties.

**Observations: Satisfied**

  - (test_get_data.py) The script checks if the data has the expected columns and no null values (`test_0_qlib_data`). The `test_1_csv_data` function checks that the number of CSV files matches the expected count.
  - (test_dump_data.py) The script checks if the data has the expected columns and no null values (test_3_dump_features, test_4_dump_features_simple).
  - (test_pit.py) The code includes several test functions that verify the format of the data.The `check_same` method is used to compare the actual data with the expected data, ensuring that the data matches the expected format.
  - (test_index_data.py) The code includes multiple test cases that check the format of the data using the `idd.SingleData` and `idd.MultiData` classes. These tests cover various scenarios such as auto broadcasting for scalar values, handling empty values, checking for alignment, indexing, slicing, and handling corner cases. The tests also include assertions to verify the expected behavior, such as raising exceptions for misaligned data and checking for NaN values.
  - (test_storage.py) The code includes multiple test functions that check the format of data in various storage classes (CalendarStorage, InstrumentStorage, FeatureStorage). These tests include assertions to verify data types, iterable properties, and expected exceptions for invalid data. Specific checks include:
    - CalendarStorage: Verifies that the data and slices are iterable and handles ValueError exceptions for invalid data.
    - InstrumentStorage: Ensures that the data is iterable, keys are strings, values are tuples of length 2, and handles ValueError exceptions for invalid data.
    - FeatureStorage: Checks that the data is of the correct type (float or np.float32), verifies the length of slices, and handles IndexError and ValueError exceptions for invalid data.
- (test_handler.py) The script creates a DataHandler from the DataFrame and performs operations to check if the data is correctly loaded and formatted. This is shown in the test_handler_df function. However, it does not explicitly check the data types or other properties.
  - (test_dataset.py) The script performs operations that assume the data is in the expected format, such as accessing data by index and fetching data for specific date ranges. This is shown in the testTSDataset function
  - (test_processor.py) The provided code includes several test functions (`test_MinMaxNorm`, `test_ZScoreNorm`, `test_CSZFillna`, and `test_CSZScoreNorm`) that verify the normalization and filling of missing values in data, and then asserts that the processed data matches the expected format. The checks involve verifying the shape and values of the data after processing.
  - (test_handler_storage.py)  The script creates a TestHandler instance and performs data fetching operations, assuming the data is in the expected format. This is shown in the test_handler_storage function. However, there is no explicit verification of the data format, such as checking the shape, data types, or values.
  - (test_datalayer.py) The script performs descriptive statistics and grouping operations on the data, suggesting that the data is in the expected format. This is shown in the testCSI300 and testClose functions. The tests use descriptive statistics to verify the data properties and include assertions to ensure the data meets expected criteria.
  - (test_saoe_simple.py) The code includes several test functions that verify the format of the data. For example, `test_pickle_data_inspect` checks the length of the data and ensures it matches expected values.


**Function References:**

  - {'File Path': '../../../qlib/tests/test_get_data.py', 'Functions': ['test_0_qlib_data', 'test_1_csv_data']}
  - {'File Path': '../../../qlib/tests/test_pit.py', 'Functions': ['test_query', 'test_no_exist_data', 'test_expr', 'test_unlimit', 'test_expr2', 'test_pref_operator']}
  - {'File Path': '../../../qlib/tests/misc/test_index_data.py', 'Functions': ['test_index_single_data', 'test_index_multi_data', 'test_sorting', 'test_corner_cases', 'test_ops', 'test_squeeze']}
  - {'File Path': '../../../qlib/tests/storage_tests/test_storage.py', 'Functions': ['test_calendar_storage', 'test_instrument_storage', 'test_feature_storage']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_handler.py', 'Functions': ['test_handler_df']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_processor.py', 'Functions': ['test_MinMaxNorm', 'test_ZScoreNorm', 'test_CSZFillna', 'test_CSZScoreNorm']}
  - {'File Path': '../../../qlib/tests/dataset_tests/test_datalayer.py', 'Functions': ['testCSI300', 'testClose']}
  - {'File Path': '../../../qlib/tests/rl/test_saoe_simple.py', 'Functions': ['test_pickle_data_inspect', 'test_simulator_first_step', 'test_simulator_stop_twap', 'test_simulator_stop_early', 'test_simulator_start_middle', 'test_interpreter', 'test_network_sanity', 'test_twap_strategy', 'test_cn_ppo_strategy', 'test_ppo_train']}
  - {'File Path': '../../../qlib/tests/test_dump_data.py', 'Functions': ['test_3_dump_features', 'test_4_dump_features_simple']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_dataset.py', 'Functions': ['testTSDataset']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_handler_storage.py', 'Functions': ['test_handler_storage']}

### 3.5 Check for Duplicate Records in Data

**Requirement**: Verify that there are no duplicate records in the loaded data.

**Observations: Not Satisfied**

  - None of test function fulfilled

**Function References:**

### 4.2 Verify Data Split Proportion

**Requirement**: Check that the data is split into training and testing sets in the expected proportion. Verify the split by checking the actual fraction of data points in the training and test sets.

**Observations: Partially Satisfied**

  - (test_contrib_workflow.py) The code defines a dataset configuration with specific date ranges for training, validation, and testing sets. However, there is no explicit verification of the actual fraction of data points in the training and test sets.
  - (test_dataset.py) The script specifies the segments for training, validation, and testing data, and prepares the data accordingly. This is shown in the testTSDataset function. It does not check the actual fraction of data points in the training and test sets.

**Function References:**

  - {'File Path': '../../../qlib/tests/test_contrib_workflow.py', 'Functions': ['train_multiseg', 'train_mse']}
  - {'File Path': '../../../qlib/tests/data_mid_layer_tests/test_dataset.py', 'Functions': ['testTSDataset']}

### 5.3 Ensure Model Output Shape Aligns with Expectation

**Requirement**: Ensure that the structure of the model's output matches the expected format based on the task, such as checking the dimensions of the output versus the number of labels in classification task.

**Observations: Satisfied**

  - (test_structured_cov_estimator.py) The provided code includes multiple test cases that validate the output of the `StructuredCovEstimator` model. These tests check if the estimated covariance matrix matches the expected covariance matrix generated by numpy's `np.cov` function.
  - (test_qlib_simulator.py) The provided code includes several test functions that validate the state and metrics of the simulator. (e.g. 'cur_time', 'position', 'history_exec', 'history_steps', and 'metrics'). However, there is no explicit check for the shape or dimensions of the model's output in relation to the expected format.
  - (test_saoe_simple.py) The provided code includes several test functions that validate the state and output of the simulator and interpreters. It also checks for the shape of the model's output in relation to the expected format based on the task (e.g. `len(metrics) == len(orders)`)

**Function References:**

  - {'File Path': '../../../qlib/tests/test_structured_cov_estimator.py', 'Functions': ['test_random_covariance', 'test_nan_option_covariance', 'test_decompose_covariance', 'test_constructed_covariance', 'test_decomposition']}
  - {'File Path': '../../../qlib/tests/rl/test_qlib_simulator.py', 'Functions': ['test_simulator_first_step', 'test_simulator_stop_twap', 'test_interpreter']}
  - {'File Path': '../../../qlib/tests/rl/test_saoe_simple.py', 'Functions': ['test_twap_strategy', 'test_cn_ppo_strategy', 'test_ppo_train']}

### 6.1 Verify Evaluation Metrics Implementation

**Requirement**: Verify that the evaluation metrics are correctly implemented and appropriate for the model's task. Verify the metric computations with expected values to validate correctness.

**Observations: Satisfied**

  - (test_all_pipeline.py) The 'test_0_train' method in the 'TestAllFlow' class asserts that IC (Information Coefficient) and RIC (Rank IC)are greater than or equal to 0, which is a basic validation of correctness. However, there is no detailed verification against expected values to ensure the correctness of the metric computations.
  - (test_structured_cov_estimator.py) The provided code includes multiple test cases that validate the correctness of the covariance estimation by comparing the estimated covariance matrix with the one computed using numpy's cov function. The tests use assertions to check if the differences between the estimated and actual covariance matrices are within a specified tolerance (EPS).
  - (test_file_strategy.py) The code checks if the computed 'ffr' (fill factor ratio)  values match the expected values for specific dates. This indicates that the evaluation metrics are being verified for correctness.
  - (test_qlib_simulator.py) The code (e.g. functions `test_simulator_first_step`, `test_simulator_stop_twap`, and `test_interpreter`) includes several test functions that validate the correctness of the evaluation metrics (e.g. `market_volume`, `market_price`, `trade_price`, `position`, and `ffr`). These assertions compare the computed values against expected values using the `is_close` function to ensure accuracy.
  - (test_saoe_simple.py) The code includes several test functions that validate the correctness of evaluation metrics. For example, `test_simulator_stop_twap` checks various metrics such as `ffr`, `market_price`, `trade_price`, and `pa` against expected values. Similarly, `test_twap_strategy` and `test_cn_ppo_strategy` validate metrics like `ffr`, `pa`, `market_price`, and `trade_price` by comparing them to expected values using assertions.
  - (test_trainer.py) The code (e.g. the `test_trainer` function) asserts that the `trainer.metrics['acc']` is consistent with `trainer.metrics['reward'] * 100` and checks that the accuracy is above certain thresholds after training and testing. However, there is no explicit verification of the metric computations with expected values beyond these assertions.


**Function References:**

  - {'File Path': '../../../qlib/tests/test_all_pipeline.py', 'Functions': ['test_0_train']}
  - {'File Path': '../../../qlib/tests/test_structured_cov_estimator.py', 'Functions': ['test_random_covariance', 'test_nan_option_covariance', 'test_decompose_covariance', 'test_constructed_covariance', 'test_decomposition']}
  - {'File Path': '../../../qlib/tests/backtest/test_file_strategy.py', 'Functions': ['test_file_str']}
  - {'File Path': '../../../qlib/tests/rl/test_qlib_simulator.py', 'Functions': ['test_simulator_first_step', 'test_simulator_stop_twap', 'test_interpreter']}
  - {'File Path': '../../../qlib/tests/rl/test_saoe_simple.py', 'Functions': ['test_simulator_stop_twap', 'test_twap_strategy', 'test_cn_ppo_strategy']}
  - {'File Path': '../../../qlib/tests/rl/test_trainer.py', 'Functions': ['test_trainer']}

### 6.2 Evaluate Model's Performance Against Thresholds

**Requirement**: Compute evaluation metrics for both the training and testing datasets. Verify that these metrics exceed threshold values, indicating acceptable model performance.

**Observations: Satisfied**

  - (test_all_pipeline.py) The code includes functions that train the model and evaluate its performance. Specifically, the `test_0_train` method in the `TestAllFlow` class computes evaluation metrics for the training dataset and checks if they exceed threshold values. The `test_1_backtest` method evaluates the model's performance on the testing dataset and verifies that the annualized return exceeds a threshold value of 0.05.
  - (test_trainer.py) The code (e.g. `test_trainer` function) computes metrics such as 'acc' and 'reward' for both training and testing datasets and checks if they exceed certain thresholds (e.g., `assert trainer.metrics['acc'] > 80` for training and `assert trainer.metrics['acc'] > 60` for testing).

**Function References:**

  - {'File Path': '../../../qlib/tests/test_all_pipeline.py', 'Functions': ['test_0_train', 'test_1_backtest']}
  - {'File Path': '../../../qlib/tests/rl/test_trainer.py', 'Functions': ['test_trainer', 'test_trainer_earlystop']}