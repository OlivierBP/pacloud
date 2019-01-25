#! /bin/sh
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT
#
# Script to push in a S3 bucket all the stuff needed for the Pacloud Project
# Need to create a user with programmatic access and S3 policies
# Configure the credentials on the local computer with "aws configure"


set -e

# S3 Bucket
bucket=pacloud


# Zip the lambda function and upload them
if [ -d "Lambda" ]; then
    cd Lambda

    echo "Zipping Lambda function..."
    zip PackageRequest.zip PackageRequest.js
    zip CustomResource_SpotFleet.zip CustomResource_SpotFleet.js

    echo "Uploading Lambda functions..."
    aws s3 cp PackageRequest.zip s3://$bucket/Lambda/
    aws s3 cp CustomResource_SpotFleet.zip s3://$bucket/Lambda/

    echo "Lambda functions uploaded"
    cd ..
else
    echo "Warning: Can't find Lambda directory"
fi


# Upload the CloudFormation templates in S3
if [ -d "CloudFormation" ]; then

    echo "Uploading CloudFormation templates..."
    aws s3 cp --recursive CloudFormation s3://$bucket/CloudFormation

    echo "CloudFormation templates uploaded"
else
    echo "Warning: Can't find CloudFormation directory"
fi


# Upload the AMI folder in S3
if [ -d "AMI" ]; then

    echo "Uploading AMI folder..."
    aws s3 cp --recursive AMI s3://$bucket/AMI

    echo "AMI folder uploaded"
else
    echo "Warning: Can't find AMI directory"
fi


# Put in the clip board the path to the main.yaml
echo https://s3-eu-west-1.amazonaws.com/pacloud/CloudFormation/main.yaml | xclip -selection clipboard

echo "Done"


# To retrieve from S3 via awscli:
#aws s3 cp --recursive s3://pacloud/AMI/ /pacloud/AMI/
