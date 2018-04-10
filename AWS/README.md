# AWS Server part

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
├── Diagrams  
│   ├── Architecture.xml  
│   └── Process_architecture.xml  
├── Lambda  
│   ├── CustomResource_SpotFleet.js  
│   ├── CustomResource_SpotFleet.zip  
│   ├── PackageRequest.js  
│   ├── PackageRequest.zip  
│   ├── SyncClientDb.js  
│   └── SyncClientDb.zip  
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

Need to change the AMI in the EC2.yaml template in the "Mappings" part:
>SpotInstanceRegionArch2AMI:  
>   eu-west-1:  
>      '64': **ami-05461d7c**  




1. Upload the templates in S3
    ```SHELL
    # Need to upload the templates in S3
    cd Pacloud/AWS/
    ./uploadInS3.sh
    ```
1. Create S3Buckets.yaml stack
1. Create DynamoDB.yaml stack
2. Create main.yaml stack
    * Automatically deploy nested stack Serverless.yaml
    * Automatically deploy nested stack network.yaml
    * Automatically deploy nested stack Ec2.yaml
3. Create stack SpotFleet.yaml


## Other

### Connection to a spot instance through the bastion server with local keys

```SHELL
ssh -i ~/Bureau/KeyPair_Server1.pem -o ProxyCommand='ssh -i ~/Bureau/KeyPair_Server1.pem -W %h:%p ubuntu@34.244.176.197' ubuntu@10.0.0.38
```

