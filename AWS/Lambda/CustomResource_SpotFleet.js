// Pacloud project
// CustomResource SpotFleet Lambda function
// https://github.com/OlivierBP/Pacloud
// Created 2018-03-27 by BAL-PETRE Olivier
// License MIT

// Best practices CustomResource in CloudFormation
// https://aws.amazon.com/premiumsupport/knowledge-center/best-practices-custom-cf-lambda/

'use strict';

// The handler
exports.lambda_handler = function(event, context) {
  try {
    console.log(JSON.stringify(event, null, '  '));

    // DELETE
    if (event.RequestType == 'Delete') {
      deleteSpotFleet(event, function(err, result) {
        var status = err ? 'FAILED' : 'SUCCESS';
        return sendResponse(event, context, "SUCCESS", result, err);
      });
    }

    // UPDATE
    else if (event.RequestType == 'Update') {
      // Delete first
      deleteSpotFleet(event, function(err, result) {
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
function deleteSpotFleet(event, callback) {

  var aws = require("aws-sdk");
  var ec2 = new aws.EC2();
  var cloudformation = new aws.CloudFormation();

  var regex = /\/(.*)\//;
  var params = {
    StackName: event.StackId.match(regex)[1]
  };

  // Describe the stack that created the spotfleet
  cloudformation.describeStacks(params, function(err, data) {
    if (err) {
      console.log(err, err.stack);
    }
    else {
      // Retrieve the ID of the spotfleet
      var spotFleetId = data.Stacks[0].Outputs.find(o => o.OutputKey === 'SpotFleetRequestId').OutputValue;
      console.log(spotFleetId);

      var paramsCancel = {
        SpotFleetRequestIds: [
           spotFleetId
        ],
        TerminateInstances: true
       };

      // Cancel the spotfleet request
      ec2.cancelSpotFleetRequests(paramsCancel, function(errCancel, dataCancel) {
        if (errCancel){
          console.log(errCancel, errCancel.stack);
        }
        else{
          console.log(dataCancel);
          return callback(null, dataCancel);
        }
      });
    }
  });
}


// The create function
function createSpotFleet(properties, callback) {

  // Check if the property exists
  if (!properties.AllocationStrategy)
    callback({message: "AllocationStrategy not specified"});
  if (!properties.ExcessCapacityTerminationPolicy)
    callback({message: "ExcessCapacityTerminationPolicy not specified"});
  if (!properties.IamFleetRole)
    callback({message: "IamFleetRole not specified"});
  if (!properties.ReplaceUnhealthyInstances)
    callback({message: "ReplaceUnhealthyInstances not specified"});
  if (!properties.TargetCapacity)
    callback({message: "TargetCapacity not specified"});
  if (!properties.TerminateInstancesWithExpiration)
    callback({message: "TerminateInstancesWithExpiration not specified"});
  if (!properties.Type)
    callback({message: "Type not specified"});

  if (!properties.LaunchSpecifications[0])
    callback({message: "LaunchSpecifications[0] not specified"});
  if (!properties.LaunchSpecifications[0].InstanceInterruptionBehavior)
    callback({message: "LaunchSpecifications[0].InstanceInterruptionBehavior not specified"});
  if (!properties.LaunchSpecifications[0].IamInstanceProfile.Arn)
    callback({message: "LaunchSpecifications[0].IamInstanceProfile.Arn not specified"});
  if (!properties.LaunchSpecifications[0].ImageId)
    callback({message: "LaunchSpecifications[0].ImageId not specified"});
  if (!properties.LaunchSpecifications[0].InstanceType)
    callback({message: "LaunchSpecifications[0].InstanceType not specified"});
  if (!properties.LaunchSpecifications[0].KeyName)
    callback({message: "LaunchSpecifications[0].KeyName not specified"});
  if (!properties.LaunchSpecifications[0].Monitoring.Enabled)
    callback({message: "LaunchSpecifications[0].Monitoring.Enabled not specified"});
  if (!properties.LaunchSpecifications[0].SecurityGroups)
    callback({message: "LaunchSpecifications[0].SecurityGroups not specified"});
  if (!properties.LaunchSpecifications[0].SubnetId)
    callback({message: "LaunchSpecifications[0].SubnetId not specified"});
  if (!properties.LaunchSpecifications[0].TagSpecifications)
    callback({message: "LaunchSpecifications[0].TagSpecifications not specified"});



  var aws = require("aws-sdk");
  var ec2 = new aws.EC2();



  // use the (param == true) to cast in boolean
  var params = {
    SpotFleetRequestConfig: {
      IamFleetRole: properties.IamFleetRole,
      TargetCapacity: properties.TargetCapacity,
      AllocationStrategy: properties.AllocationStrategy,
      ExcessCapacityTerminationPolicy: properties.ExcessCapacityTerminationPolicy,
      InstanceInterruptionBehavior: properties.LaunchSpecifications[0].InstanceInterruptionBehavior,
      LaunchSpecifications: [
        {
          EbsOptimized: (properties.LaunchSpecifications[0].EbsOptimized == 'true'),
          IamInstanceProfile: {
            Arn: properties.LaunchSpecifications[0].IamInstanceProfile.Arn,
          },
          ImageId: properties.LaunchSpecifications[0].ImageId,
          InstanceType: properties.LaunchSpecifications[0].InstanceType,
          KeyName: properties.LaunchSpecifications[0].KeyName,
          Monitoring: {
            Enabled: (properties.LaunchSpecifications[0].Monitoring.Enabled == 'true')
          },
          SecurityGroups: [
            {
              GroupId: String(properties.LaunchSpecifications[0].SecurityGroups[0].GroupId)
            }
          ],
          SubnetId: properties.LaunchSpecifications[0].SubnetId,
          // TagSpecifications: [
          //   {
          //     ResourceType: customer-gateway | dhcp-options | image | instance | internet-gateway | network-acl | network-interface | reserved-instances | route-table | snapshot | spot-instances-request | subnet | security-group | volume | vpc | vpn-connection | vpn-gateway,
          //     Tags: [
          //       {
          //         Key: 'STRING_VALUE',
          //         Value: 'STRING_VALUE'
          //       },
          //       /* more items */
          //     ]
          //   },
          //   /* more items */
          // ],
        },
        /* more items */
      ],
      // ReplaceUnhealthyInstances: true ,
      // SpotPrice: 'STRING_VALUE',
      TerminateInstancesWithExpiration: (properties.TerminateInstancesWithExpiration == 'true'),
      Type: properties.Type,
      // ValidUntil: new Date || 'Wed Dec 31 1969 16:00:00 GMT-0800 (PST)' || 123456789
    },
  };

  ec2.requestSpotFleet(params, function(err, data) {
    if (err){
      console.log(err, err.stack);
      return callback(err);
    }
    else {
      console.log(data);
      return callback(null, data);
    }
  });
}





// Send response to the pre-signed S3 URL
function sendResponse(event, context, responseStatus, responseData, err) {
    console.log("Sending response " + responseStatus);
    var reason = err ? err.message : '';
    var responseBody = JSON.stringify({
        Status: responseStatus,
        Reason: reason + " See the details in CloudWatch Log Stream: " + context.logStreamName,
        PhysicalResourceId: context.logStreamName,
        // PhysicalResourceId: responseData.SpotFleetRequestId,
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
