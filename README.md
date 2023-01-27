
## Creating SageMaker Pipelines for training, consuming and monitoring your batch use cases

## Introduction/ Problem statement:

Batch inference is a common pattern where prediction requests are batched together on input, a job runs to process those requests against a trained model, and the output includes batch prediction responses that can then be consumed by other applications or business functions. Running batch use cases in production environments requires a repeatable process for model retraining as well as batch inference. That process should also include monitoring of that model to measure performance over time. In this blog, you’ll learn how to create repeatable pipelines for your batch use cases using Amazon SageMaker Pipelines, Amazon SageMaker Model Registry, Amazon SageMaker Batch Transform Jobs, and Amazon SageMaker Model Monitor.

There are multiple scenarios for performing batch inference. In some cases, you may be retraining your model every time you do batch inference. Alternatively, you may have the scenarios where you are training your model less frequently than you are performing batch inference. In this blog, we will focus on the second scenario. For this example, let’s assume that you have a model that is trained periodically, roughly once per month. However, batch inference is performed against the latest model version on a daily basis. In this scenario, you see a common pattern where the model training lifecycle is difference than the batch inference lifecycle.

## Batch Model Monitoring Pipelines repo

The batch-model-monitoring-pipelines repository contains the code for preprocessing, training, evaluating the model, setting baseline, and running batch transform for model monitor. It has 3 notebooks - for setup, for train & baseline pipeline, and for batch inference & model monitor. There are some helper codes.

\\|- Custom_IAM_policies
\\| |— Custom_IAM_roles_policy
\\| |— Custom_Lambda_policy
\\|— pipeline_scripts
\\| |— evaluate.py
\\| |— preprocessing.py
\\|— 0.Setup.ipynb*
\\|— 1.SageMakerPipeline-BaselineData-Train.ipynb*
\\|— 2.SageMakerPipeline-ModelMonitoring-DataQuality-BatchTransform.ipynb*
\\|— iam_helper.py
\\|— lambda_getapproved_model.py

## Prerequisites

There are some permission policies (as below) which are required by the SageMaker Execution Role for the workflow. These permission policies can be enabled through AWS Identity and Access Management (IAM) role permissions. 

// AmazonSageMaker-ExecutionPolicy-<...>	
// Custom_IAM_roles_policy	
// Custom_Lambda_policy	
// CloudWatchLogsFullAccess
// AmazonSageMakerFullAccess

AmazonSageMaker-ExecutionPolicy-<...> is the execution role associated with SageMaker user and has necessary S3 bucket policies. Custom_IAM_roles_policy and Custom_Lambda_policy are two custom policies created to support the required actions for lambda function and are saved in this folder, Custom_IAM_policies.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

