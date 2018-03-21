#! /bin/sh

# Need the package "awscli"

# Script to push in a S3 bucket all the stuff needed for the Pacloud Project
# Need to create a user with programmatic access and S3 policies
# Configure the credentials on the local computer with "aws configure"


# S3 Bucket
bucket=pacloud


# Zip the lambda function and upload them
if [ -d "Lambda" ]; then
    cd Lambda
    
    echo "Zipping Lambda function..."
    zip PackageRequest.zip PackageRequest.js
    zip SyncClientDb.zip SyncClientDb.js

    echo "Uploading Lambda functions..."
    aws s3 cp PackageRequest.zip s3://$bucket/Lambda/
    aws s3 cp SyncClientDb.zip s3://$bucket/Lambda/

    echo "Lambda functions uploaded"
    cd ..
else
    echo "Warning: Can't find Lambda directory"
fi


# Upload the CloudFormation templates in S3
if [ -d "CloudFormation" ]; then
    cd CloudFormation

    echo "Uploading CloudFormation templates..."
    aws s3 cp main.yaml s3://$bucket/CloudFormation/
    aws s3 cp Serverless.yaml s3://$bucket/CloudFormation/
    aws s3 cp Network.yaml s3://$bucket/CloudFormation/
    aws s3 cp Ec2.yaml s3://$bucket/CloudFormation/

    echo "CloudFormation templates uploaded"
    cd ..
else
    echo "Warning: Can't find CloudFormation directory"
fi


# Put in the clip board the path to the main.yaml
echo https://s3-eu-west-1.amazonaws.com/pacloud/CloudFormation/main.yaml | xclip -selection clipboard

echo "Done"

