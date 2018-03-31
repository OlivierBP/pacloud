// Pacloud project
// CustomResource SpotFleet Lambda function PROTOTYPE
// https://github.com/OlivierBP/Pacloud
// Created 2018-03-27 by BAL-PETRE Olivier
// License MIT 

// Best practices CustomrREsource in CloudFormation
// https://aws.amazon.com/premiumsupport/knowledge-center/best-practices-custom-cf-lambda/

'use strict';

  // The handler
  exports.lambda_handler = function(event, context) {
    try {
      console.log(JSON.stringify(event, null, '  '));
    
      // DELETE
      if (event.RequestType == 'Delete') {
        deleteSpotFleet(event.ResourceProperties, function(err, result) {
          var status = err ? 'FAILED' : 'SUCCESS';
          return sendResponse(event, context, "SUCCESS", result, err);
        });
      }

      // UPDATE
      else if (event.RequestType == 'Update') {
        // Delete first
        deleteSpotFleet(event.ResourceProperties, function(err, result) {
          var status = err ? 'FAILED' : 'SUCCESS';
          if (err)
            return sendResponse(event, context, "FAILED", result, err);
        });
        // Then create
        createSpotFleet(event.ResourceProperties, function(err, result) {
          var status = err ? 'FAILED' : 'SUCCESS';
          return sendResponse(event, context, status, result, err);
        });
      }

      // CREATE
      else if (event.RequestType == 'Create') {
        createSpotFleet(event.ResourceProperties, function(err, result) {
          var status = err ? 'FAILED' : 'SUCCESS';
          return sendResponse(event, context, status, result, err);
        });
    
      }

      else{
        return sendResponse(event, context, "FAILED", event);
      }
    }
    catch(err) {
      console.log("error");
      return sendResponse(event, context, "FAILED", event);
    } 
  };



  
  // The delete function
  function deleteSpotFleet(properties, callback) {

    var aws = require("aws-sdk");
    var ec2 = new aws.EC2();
  
  
    return callback(null, ec2);
  }
  

// The create function
function createSpotFleet(properties, callback) {
  if (!properties.test)
    callback({message: "test not specified"});
  if (!properties.testb)
    callback({message: "testb not specified"});
  if (!properties.testb.testc)
    callback({message: "testb.testc not specified"});


  var aws = require("aws-sdk");
  var ec2 = new aws.EC2();


  return callback(null, ec2);
}
  
  
  
  
  
  // Send response to the pre-signed S3 URL 
  function sendResponse(event, context, responseStatus, responseData, err) {
      console.log("Sending response " + responseStatus);
      var reason = err ? err.message : '';
      var responseBody = JSON.stringify({
          Status: responseStatus,
          Reason: reason + " See the details in CloudWatch Log Stream: " + context.logStreamName,
          PhysicalResourceId: context.logStreamName,
          StackId: event.StackId,
          RequestId: event.RequestId,
          LogicalResourceId: event.LogicalResourceId,
          Data: responseData
      });
  
      console.log("RESPONSE BODY:\n", responseBody);
  
      var https = require("https");
      var url = require("url");
  
      var parsedUrl = url.parse(event.ResponseURL);
      var options = {
          hostname: parsedUrl.hostname,
          port: 443,
          path: parsedUrl.path,
          method: "PUT",
          headers: {
              "content-type": "",
              "content-length": responseBody.length
          }
      };
  
      console.log("SENDING RESPONSE...\n");
  
      var request = https.request(options, function(response) {
          console.log("STATUS: " + response.statusCode);
          console.log("HEADERS: " + JSON.stringify(response.headers));
          // Tell AWS Lambda that the function execution is done  
          context.done();
      });
  
      request.on("error", function(error) {
          console.log("sendResponse Error:" + error);
          // Tell AWS Lambda that the function execution is done  
          context.done();
      });
    
      // write data to request body
      request.write(responseBody);
      request.end();
  }
