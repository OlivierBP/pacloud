// Pacloud project
// PackageRequest Lambda function
// https://github.com/OlivierBP/Pacloud
// Created 2018-03-21 by BAL-PETRE Olivier
// License MIT 

// Official documentation
// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html#sendMessage-property

'use strict';

const AWS = require('aws-sdk');             // Load the AWS SDK for Node.js
AWS.config.update({region: 'eu-west-1'});   // Set the region 

const sqs = new AWS.SQS();
const QueueName = 'QueueToCompile';         // Name of the queue

// Function called when the Lambda function is called
exports.lambda_handler = (event, context, callback) => {

    // TODO: test if the package exist in DynamoDB, if yes, return the URL of the binaries to download it

    let params_getQueueUrl = {
        QueueName: QueueName
      };
    // Retrieve the queue from its name
    sqs.getQueueUrl(params_getQueueUrl, function(err, data) {
        if (err){
            // an error occurred
            console.log('Failed to get the SQS queue');
            console.log(err, err.stack);
        }
        else {
            // successful response
            console.log('Got the SQS queue');
            console.log(data);
            console.log(data.QueueUrl);

            let params_sendMessage = {
                MessageBody: event.name,
                QueueUrl: data.QueueUrl,
                DelaySeconds: 0
            };
            // Send the message
            sqs.sendMessage(params_sendMessage, function(err, data) {
                if (err){
                    // an error occurred when sending the message
                    console.log('an error occurred when sending the message');
                    console.log(err, err.stack);
                } 
                else{
                    // successful response
                    console.log('Message sent successfully')
                    console.log(data);

                    // TODO remove these lines
                    console.log('Event:', JSON.stringify(event));
                    const name = event.name || 'NONE';
                    const response = {response: `You requested the package ${name}`};
                    callback(null, response);

                }
            });
        }
    });

};