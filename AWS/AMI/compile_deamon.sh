#! /bin/sh

# This script get a compilation request from the SQS queue, work on, upload the result in S3 and delete the task from the queue
# Require "awscli"

# Install of "awscli" for gentoo:
# emerge dev-python/pip
# pip install pip --user
# ./.local/bin/aws s3 ls (or add to the path)
# Need to set a region: aws configure set region eu-west-1

# Name of the queue
queueName=QueueToCompile

# Bucket name
bucketName=pacloud-serverless-s3m62kwuctt6-s3bucketpacloud-17f2h0ur4htqs


# Get the queue URL
queueUrl=$(aws sqs get-queue-url --queue-name $queueName | jq -r '.QueueUrl')


# Get a message from the queue
message=$(aws sqs receive-message --queue-url $queueUrl)



# If there is a message (message is null if not any was received)
if [ -n "$message" ]; then
    echo $message | jq
    # TODO Change visibility

    #echo $message | jq -r '.Messages[].Body'
    body=$(echo $message | jq -r '.Messages[].Body')
    touch /tmp/$body.tbz2
    aws s3 cp /tmp/$body.tbz2 s3://$bucketName/

    # TODO Delete message

else
    echo "Not any message for now..."
fi
    













