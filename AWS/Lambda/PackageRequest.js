// Pacloud project
// PackageRequest Lambda function
// https://github.com/OlivierBP/Pacloud
// Created 2018-03-21 by BAL-PETRE Olivier
// License MIT 

// Official documentation javascript SDK
// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/

'use strict';

const AWS = require('aws-sdk');             // Load the AWS SDK for Node.js
AWS.config.update({region: 'eu-west-1'});   // Set the region 

const sqs = new AWS.SQS();
const QueueName = 'QueueToCompile';         // Name of the queue

const dynamodb = new AWS.DynamoDB();
const TableName = 'PacloudPackages';        // Name of the DynamoDB table


// Function called when the Lambda function is called
exports.lambda_handler = (event, context, callback) => {

    // Test if a name was sent
    if ((! event.package) || (! event.version)){
        callback('ERROR: Not any package or version given');
    }
    else{
        let params_getQueueUrl = {
            QueueName: QueueName
        };
        // Retrieve the queue from its name
        sqs.getQueueUrl(params_getQueueUrl, function(err, data_getQueueUrl) {
            if (err){
                console.log('Failed to get the SQS queue:', err, err.stack);
            }
            else {
                let nameLong = event.package;
                let category = nameLong.match(/(.*)\//)[1];
                let nameShort = nameLong.match(/.*\/(.*)/)[1];
                let version = event.version;
                let useflag = event.useflag || " ";
                let packageExpression = nameLong + '-' + version;

                let params_getItem = {
                        Key: {
                            "package": {
                                S: packageExpression
                            }, 
                            "useflagCompiled": {
                                S: useflag
                            }
                        }, 
                    TableName: TableName
                };
                // Search the item in DynamoDB
                dynamodb.getItem(params_getItem, function(err, data_getItem) {
                    if (err) {
                        console.log('Failed to get an item from dynamodb:', err, err.stack);
                    }
                    else{
                        // WAIT: No item, request a compilation
                        if (! data_getItem.hasOwnProperty('Item')){
                            let messageBody = JSON.stringify(
                                {
                                    "packageExpression": packageExpression,
                                    "nameLong": nameLong,
                                    "category": category,
                                    "nameShort": nameShort,
                                    "version": version,
                                    "useflag": useflag
                                }
                            )
                            let params_sendMessage = {
                                MessageBody: messageBody,
                                QueueUrl: data_getQueueUrl.QueueUrl,
                                DelaySeconds: 0
                            };
                            // Send the compilation request in the SQS queue
                            sqs.sendMessage(params_sendMessage, function(err, data_sendMessage) {
                                if (err){
                                    console.log('Failed to send the message in the SQS queue:', err, err.stack);
                                } 
                                else{
                                    var params_putItem = {
                                        Item: {
                                            "package": {
                                                S: packageExpression
                                            }, 
                                            "useflagCompiled": {
                                                S: useflag
                                            },
                                            "compiling": {
                                                S: String(Date.now())
                                            }
                                        }, 
                                        TableName: TableName
                                       };
                                       // Put a line for this package in the DynamoDB table
                                       dynamodb.putItem(params_putItem, function(err, data_putItem) {
                                         if (err){
                                             console.log('Failed to insert in the DynamoDB table:', err, err.stack);
                                         }
                                         else{
                                            const response = {status: "WAIT"};
                                            callback(null, response);
                                         }
                                    });
                                }
                            });
                        }

                        // SUCCESS: Package already compiled, return the S3 URL
                        else if (data_getItem.Item.hasOwnProperty('linkS3')){
                            const response = {status: "SUCCESS", linkS3: data_getItem.Item.linkS3.S};
                            callback(null, response);
                        }

                        // WAIT: Package already requested for compilation
                        else if (data_getItem.Item.hasOwnProperty('compiling')){
                            const response = {status: "WAIT"};
                            callback(null, response);
                        }

                        // FAILED: The package failed to compile
                        else if (data_getItem.Item.hasOwnProperty('errorMessage')){
                            const response = {status: "FAILED", errorMessage: data_getItem.Item.errorMessage.S};
                            callback(null, response);
                        }

                    } // dynamodb.getItem error?
                }); // dynamodb.getItem

            } //sqs.getQueueUrl error?
        }); //sqs.getQueueUrl

    } // Test if name given
};
