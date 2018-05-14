# AWS Server part

## Architecture

### Request process

![Process architecture](https://s3-eu-west-1.amazonaws.com/olivierbp/Process_architecture.png)

This is the simplified process behind a user request. When a user request a package through the pacloud client, a HTTP request is sent to the API and forwarded to a Lambda function. The Lambda function will check in a DynamoDB table if the package was already compiled with exactly the same parameters. If it was, a URL is returned to the client to download the binary from a S3 bucket and it will be installed. If it was not compiled yet, a message is put in a SQS queue.  
A fleet of Spot instances checks regularly if there is something to compile in the queue and does it when appropriate. Once compiled, the binary is put in S3 and the meta-data are put in the DynamoDB table. Then, the SQS message is deleted.

### Spot instance

![Spot instance](https://s3-eu-west-1.amazonaws.com/olivierbp/AMI_architecture_worker.png)

The compilation tasks required a lot of computing power. That's the reason why we wanted to put it in the Cloud, but it can also be expensive. To keep a low cost, the Spot instance model was chosen. However, the Spot instances can be requested back and doesn't let us the time to finish the current compilation. To avoid to loose any work done, we can hibernate the instance and resume it later when the instance is available again. This feature is new and has [a lot of restrictions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html). One of them is the need to have a hibernation agent running on the instance. This agent is only provided for Linux OSes Ubuntu and Amazon Linux. That's why the OS chosen is Ubuntu. To get Portage to compile the packages, we run periodically a [Gentoo stage 3 container](https://hub.docker.com/r/gentoo/stage3-amd64/). The container is destroyed after each compilation to always get the same compilation environment.

### Compilation command

This is the compilation command executed in the Gentoo container:

```BASH
env USE="$useflag" \            # Set the USE flags for only this command
    emerge \
    --onlydeps \                # Compile only the dependencies and not the package
    --onlydeps-with-rdeps n \   # Compile just the build time dependencies and not the run time dependencies
    =$package-$version \        # Package and version
    && emerge --buildpkgonly =$package-$version     #  Build a binary for the package and don’t install the package. Use "&&" and not another instruction will not execute the second part if the first one fails
```

### Computing resources architecture

![Computing resources architecture](https://s3-eu-west-1.amazonaws.com/olivierbp/Computing_resources_architecture.png)

NAT instances security group (inbound rules):

| Protocol type | Port number |     Source IP     |
| ------------- | ----------- | ----------------- |
|     TCP       |     80      | spot-instances-sg |
|     TCP       |     80      | spot-instances-sg |

Spot instances security group (inbound rules):

| Protocol type | Port number |     Source IP     |
| ------------- | ----------- | ----------------- |
|     TCP       |     22      |     bastion-sg    |

As the schema above shows, all the Spot instances are in private subnets and use a NAT instance to get an Internet access. A bastion server was added to get a SSH access to the Spot Instances if needed. The one-line SSH command can be found [here](#connect-to-a-spot-instance-through-the-bastion-server-with-local-keys). Notice that the two keys are kept local and not any need to be store in the Bastion server.  

The CloudFormation stacks creates the architecture in three AZ (availability zones) to ensure a high availability. The Spot Fleet can put the Spot instances in a way to maximise the dispersion in the AZ and maximise the availability or in a way the optimise the price of the instances. This parameter is chosen when launching the CloudFormation stack "main.yaml".


## Deploy the Server

### Folder architecture

Pacloud/AWS/  
.  
├── AMI  
│   ├── createAMI_Ubuntu.sh  
│   ├── Dockerfile  
│   └── scripts  
│       ├── compilePackage.sh  
│       ├── cronJob.sh  
│       └── setMakeConf.sh  
├── CloudFormation  
│   ├── DynamoDB  
│   │   └── DynamoDB.yaml  
│   ├── Ec2.yaml  
│   ├── main.yaml  
│   ├── Network.yaml  
│   ├── S3Buckets  
│   │   └── S3Buckets.yaml  
│   ├── Serverless.yaml  
│   └── SpotFleet  
│       └── SpotFleet.yaml  
├── Diagrams ***(to open with [draw.io](https://draw.io))***  
│   └── ...  
├── Lambda  
│   ├── CustomResource_SpotFleet.js  
│   ├── PackageRequest.js  
├── README.md  
├── scpAMI.sh  
└── uploadInS3.sh  


### Create the Docker container

```SHELL
# Create the container
cd Pacloud/AWS/AMI/
docker build -f Dockerfile -t olivierbp/pacloud .
docker run --rm --cap-add=SYS_PTRACE olivierbp/pacloud:latest

# Commit and push the container to DockerHub
docker login --username olivierbp
docker commit -a "olivierbp" -m "message" containerId olivier/pacloud:tags
docker push olivierbp/pacloud:tags
```

### Create the Ubuntu worker AMI

In a EC2 with an Ubuntu AMI (tested with Ubuntu 16.04 LTS HVM):

```SHELL
./Pacloud/AWS/AMI/createAMI_Ubuntu.sh
```

### Create the server architecture with CloudFormation

Need to change the AMI in the EC2.yaml template in the "Mappings" part to put the one you created:
>SpotInstanceRegionArch2AMI:  
>   eu-west-1:  
>      '64': **ami-05461d7c**  


1. Upload the templates in S3
    ```SHELL
    # Need to upload the templates in S3
    cd Pacloud/AWS/
    ./uploadInS3.sh
    ```
2. Create S3Buckets.yaml stack
3. Create DynamoDB.yaml stack
4. Create main.yaml stack
    * Automatically deploy nested stack Serverless.yaml
    * Automatically deploy nested stack network.yaml
    * Automatically deploy nested stack Ec2.yaml
5. Create stack SpotFleet.yaml


## Utilities

### Connect to a Spot instance through the bastion server with local keys

```SHELL
ssh -i ~/Path/to/KeyPair1.pem -o ProxyCommand='ssh -i ~/Path/to/KeyPair2.pem -W %h:%p ubuntu@34.244.176.197' ubuntu@10.0.0.38
```

