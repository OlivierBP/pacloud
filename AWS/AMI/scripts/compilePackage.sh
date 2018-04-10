#! /bin/sh

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
    aws sqs change-message-visibility --queue-url $queueUrl --visibility-timeout 600 --receipt-handle $receiptHandle
    echo "Message visibility changed"

    #echo $message | jq -r '.Messages[].Body'
    body=$(echo $message | jq -r '.Messages[].Body')

    package=$(echo $body | sed 's/\-[0-9].*//')
    packageReg=$(echo $package | sed 's/\//\\\//')
    version=$(echo $body | sed "s/$packageReg-//")
   
    # Before compile, set the make.conf
    /pacloud/AMI/scripts/setMakeConf.sh
    
    errorMessage=""
    # Compilation in a background process and redirect all the errors in $errorMessage
#ERROR=$(./useless.sh 2>&1 >/dev/null)
    errorMessage=$(/pacloud/AMI/scripts/emergeCommand.sh $package $version 2>&1 >/dev/null &)
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
    packageFolder=$(echo $body | sed 's/.*\///')
    parentFolder=$(echo $body | sed 's/\/.*//')
    aws s3 cp /usr/portage/packages/$parentFolder/$packageFolder.tbz2 s3://$bucketName/ --acl public-read
    echo "Binary uploaded"



    # Update the entry in the DynamoDB table
    dbupdate_key=" \
        { \
            \"name\": { \
                \"S\": \"$package\" \
            }, \
            \"version\": { \
                \"S\": \"$version\" \
            } \
        }"

    # If $errorMessage is empty 
    if [[ -z $errorMessage ]]; then
        dbupdate_expressionAttributeValues=" \
            { \
                \":l\": { \
                    \"S\": \"https://s3-eu-west-1.amazonaws.com/$bucketName/$packageFolder.tbz2\" \
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
    
