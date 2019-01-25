#! /bin/sh
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT
#
# This script get a compilation request from the SQS queue, work on, upload the result in S3 and delete the task from the queue

# Name of the queue
queueName=QueueToCompile

# Bucket name
bucketName=pacloud-packages-bucket

# Name of the DynamoFb Table
dynamoDbTableName=PacloudPackages


# Get the queue URL
queueUrl=$(aws sqs get-queue-url --queue-name $queueName | jq -r '.QueueUrl')


# Get a message from the queue
message=$(aws sqs receive-message --queue-url $queueUrl)
echo $message | jq -r ''

# If there is a message (message is null if not any was received)
if [ -n "$message" ]; then

    # Get the receipt handler
    receiptHandle=$(echo $message | jq -r '.Messages[].ReceiptHandle')

    # Change visibility timeout for 10 min
    aws sqs change-message-visibility \
        --queue-url $queueUrl \
        --visibility-timeout 600 \
        --receipt-handle $receiptHandle
    echo "Message visibility changed"

    body=$(echo $message | jq -r '.Messages[].Body')
    packageExpression=$(echo $body | jq -r '.packageExpression')    # app-misc/ranger-1.8.1
    nameLong=$(echo $body | jq -r '.nameLong')                      # app-misc/ranger
    category=$(echo $body | jq -r '.category')                      # app-misc
    nameShort=$(echo $body | jq -r '.nameShort')                    # ranger
    version=$(echo $body | jq -r '.version')                        # 1.8.1
    useflag=$(echo $body | jq -r '.useflag')                        #

    # Before compile, set the make.conf
    # TODO: Needed ??
    /pacloud/AMI/scripts/setMakeConf.sh

    errorMessage=""
    # Compilation in a background process and redirect all the errors in $errorMessage
    errorMessage=$(/pacloud/AMI/scripts/emergeCommand.sh $nameLong $version $useflag 2>&1 >/dev/null &)
    [[ ! -z $errorMessage ]] && echo "Error compilation: $errorMessage"
    # PID of the background process
    PROC_ID=$!

    # While compiling, each 10 sec, reinitialise the visibility-timeout to 10 min
    while kill -0 "$PROC_ID" > /dev/null 2>&1; do
        echo "Package compiling"
        sleep 10
        aws sqs change-message-visibility --queue-url $queueUrl --visibility-timeout 600 --receipt-handle $receiptHandle
    done
    echo "Package compiled"

    # Upload the binary in S3
    uuid=$(cat /proc/sys/kernel/random/uuid)
    packageS3Name=$bucketName/$uuid-$category@$nameShort-$version.tbz2
    aws s3 cp /usr/portage/packages/$packageExpression.tbz2 s3://$packageS3Name --acl public-read
    echo "Binary uploaded"



    # Update the entry in the DynamoDB table
    dbupdate_key=" \
        { \
            \"package\": { \
                \"S\": \"$packageExpression\" \
            }, \
            \"useflagCompiled\": { \
                \"S\": \"$useflag\" \
            } \
        }"

    # If $errorMessage is empty
    if [[ -z $errorMessage ]]; then
        dbupdate_expressionAttributeValues=" \
            { \
                \":l\": { \
                    \"S\": \"https://s3-eu-west-1.amazonaws.com/$packageS3Name\" \
                } \
            }"
        dbupdate_updateExpression="SET linkS3 = :l REMOVE compiling, errorMessage"
    else
        # Escape all the bad character in the error message
        errorMessage=$(echo $errorMessage | sed 's/\"/\\\"/g')
        dbupdate_expressionAttributeValues=" \
            { \
                \":em\": { \
                    \"S\": \"$errorMessage\" \
                } \
            }"
        dbupdate_updateExpression="SET errorMessage = :em REMOVE compiling, linkS3"
    fi

    aws dynamodb update-item \
        --table-name $dynamoDbTableName\
        --key "$dbupdate_key" \
        --update-expression "$dbupdate_updateExpression" \
        --expression-attribute-values "$dbupdate_expressionAttributeValues"


    echo "Entry updated in the DynamoDb table"

    # Delete message
    aws sqs delete-message --queue-url $queueUrl --receipt-handle $receiptHandle
    echo "SQS message deleted"

else
    echo "Not any message for now..."
fi

