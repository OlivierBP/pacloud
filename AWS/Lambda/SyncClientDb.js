// Pacloud project
// SyncClientDb Lambda function
// https://github.com/OlivierBP/Pacloud
// Created 2018-03-21 by BAL-PETRE Olivier
// License MIT 

'use strict';

exports.lambda_handler = (event, context, callback) => {
  console.log('Event:', JSON.stringify(event));
  const response = {response: `Here is the list of all the packages and versions`};
  callback(null, response);
};

