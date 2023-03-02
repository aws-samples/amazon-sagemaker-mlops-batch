
"""
This Lambda function queries SageMaker Model Registry for a specific model package 
group provided on input to identify the latest approved model version and return related metadata. 
The output includes: 
(1) model package arn (2) packaged model name (3) S3 URI for statistics baseline 
(4) S3 URI for constraints baseline  
The output is then used as input into the next step in the pipeline that
performs batch monitoring and scoring using the latest approved model. 
"""

import json
import boto3
from botocore.exceptions import ClientError

import logging
import os

def lambda_handler(event, context):
    """ """
    sm_client = boto3.client("sagemaker")
    logger = logging.getLogger()
    logger.setLevel(os.getenv("LOGGING_LEVEL", logging.INFO))

    # The model package group name
    model_package_group_name = event["model_package_group_name"]
    print(model_package_group_name)
    
    try:

        approved_model_response = sm_client.list_model_packages(
            ModelPackageGroupName=model_package_group_name,
            ModelApprovalStatus="Approved",
            SortBy="CreationTime"
        )
        
        model_package_arn = approved_model_response["ModelPackageSummaryList"][0]["ModelPackageArn"]
        logger.info(f"Identified the latest approved model package: {model_package_arn}")
        
        s3_baseline_uri_response = sm_client.describe_model_package(
            ModelPackageName=model_package_arn        
        )
        
        s3_baseline_uri_statistics = s3_baseline_uri_response["ModelMetrics"]["ModelDataQuality"]["Statistics"]["S3Uri"]
        s3_baseline_uri_constraints = s3_baseline_uri_response["ModelMetrics"]["ModelDataQuality"]["Constraints"]["S3Uri"]
        model_name = s3_baseline_uri_response["CustomerMetadataProperties"]["ModelName"]
        
        logger.info(f"Identified the latest data quality baseline statistics for approved model package: {s3_baseline_uri_statistics}")
        logger.info(f"Identified the latest data quality baseline constraints for approved model package: {s3_baseline_uri_constraints}")
        
        return {
        "statusCode": 200,
        "modelArn": model_package_arn,
        "s3uriConstraints": s3_baseline_uri_constraints,
        "s3uriStatistics": s3_baseline_uri_statistics,
        "modelName": model_name
        }

    
    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(error_message)
        raise Exception(error_message)
