#! /bin/sh

# This script get a compilation request from the SQS queue, work on, upload the result in S3 and delete the task from the queue

# Name of the queue
queueName=QueueToCompile

# Bucket name
bucketName=pacloud-packages-bucket


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

    # TODO put a lock in DynamoDB too

    #echo $message | jq -r '.Messages[].Body'
    body=$(echo $message | jq -r '.Messages[].Body')

    package=$(echo $body | sed 's/\-[0-9].*//')
    version=$(echo $body | sed 's/.*-//')
   
    # Before compile, set the make.conf
    /pacloud/AMI/scripts/setMakeConf.sh
    # Compilation in a subprocess
    #/pacloud/AMI/scripts/compilePackageSubProcess.sh $package 
    emerge --buildpkgonly  =$package-$version
    echo "Package compiled"

    # Upload the binary in S3
    packageFolder=$(echo $body | sed 's/.*\///')
    parentFolder=$(echo $body | sed 's/\/.*//')
    aws s3 cp /usr/portage/packages/$parentFolder/$packageFolder.tbz2 s3://$bucketName/
    echo "Binary uploaded"

    # Delete message
    aws sqs delete-message --queue-url $queueUrl --receipt-handle $receiptHandle
    echo "Message deleted"

else
    echo "Not any message for now..."
fi
    

