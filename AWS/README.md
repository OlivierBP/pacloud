# AWS Server part

## Deploy CloudFormation stacks

1. ./uploadInS3.sh (requiered to update bucket name)
1. Create S3Buckets.yaml stack
2. Create main.yaml stack
    * Automatically deploy nested stack Serverless.yaml
    * Automatically deploy nested stack network.yaml
    * Automatically deploy nested stack Ec2.yaml
3. Create stack SpotFleet.yaml

## Create the AMI pacloud worker

1. Find a gentoo AMI
2. ./scpAMI.sh
3. ./createAMI_base.sh
4. ./createAMI_cron.sh
5. ./createAMI_hibernate.sh

### Connection to a spot instance through the bastion server with local keys

```SHELL
ssh -i ~/Bureau/KeyPair_Server1.pem -o ProxyCommand='ssh -i ~/Bureau/KeyPair_Server1.pem -W %h:%p ubuntu@34.244.176.197' ubuntu@10.0.0.38
```

## Old

### Deploy the nested templates in CloudFormation

Put all the templates in S3 (main.yaml doesn't need it) and deploy main.yaml
It can be required to update the links in main.yaml to point to the S3 URL

### Find the bandwidth of an instance
* download speedtest-cli on gentoo
* ```speedtest-cli```

## Template architecture

**S3Buckets.yaml** *-> export Buckets name and ARN*

**main.yaml** *-> import the values from S3Buckets.yaml and link the property between the nested stacks with outputs/parameters*  
 |  
 |------ Serverless.yaml  
 |  
 |------ Network.yaml  
 |  
 |------ Ec2.yaml  

