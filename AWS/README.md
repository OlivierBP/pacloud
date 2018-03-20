# Ideas

## Architecture

### Request a package

                                  CLIENT
                                    |
                                    |
                                    | request http
                                    |
                                    |
                                API GATEWAY
                                    |
                                    |
                                    |
                                    |               search
                                  LAMBDA --------------------------- DynamoDB
                                    |
                                    |
                                    |
                        exists      |      doesn't
                    -------------------------------------
                    |                                   |
                S3/CloudFront                          SQS
                (return URL)                            |
                                                        |
                                                        |
                                            ------------------------- => AUTO-SCALING
                                            |       |       |       |
                                           EC2     EC2     EC2     EC2 (on-demand to begin, maybe spot instances after)
                                            |
                                            |
                                            |
                                            | compile
                                            |
                                            |
                                -------------------------
                                |                       |
                                |                       |
       Put the compiled package |                       | Put the meta-data
                                |                       |
                            S3 bucket                DynamoDB
                                |
                                |
                                |
                            CloudFront
                                |
                                |
                                |
                        (can return URL)




### Download package

                                  CLIENT
                                    |
                                    |
                                    |
                                CloudFront



### Automatic refresh of the packages database

                                CRON TIMER (each 2 min -- integrated to lambda)
                                    |
                                    |
                                    |
                                  LAMBDA <--------------------- retrieve the packages from internet
                                    |
                    -------------------------------------
                    |                                   |
                    |                                   |
                    | Add the new packages              | If there is a new version of a package already downloaded, request a compilation
                    |     and new versions              |
                    |                                   |
                DynamoDB                               SQS (the same than in schema 1)
                                                        |
                                                        |
                                                        |
                                                       EC2








## Questions

* Faut-il notifier quand un paquet est compilé ? Si en background, NON, si compilation + installation, OUI (la connexion est gardée ouverte et on envoie les URL au fur et à mesure)
    Faut-il notifier quand un groupe de paquet est compilé (ex: tous ce demandés lors d'une maj ?  
    => Si oui, où mettre le déclenchement pour SNS ?


* Comment le server connait tous les paquets ? Connait-il tous les paquets ? OUI


## API Gateway

* **GET Package, keep connection alive**
    * name
    * version
    * compile options (...)

* **GET Package, close the connection (compile in background)**
    * name
    * version
    * compile options (...)


* **GET Refresh packages database**
    * ???


## DynamoDB

=> Need to define

Table tous les paquets
Name: string
Version tableau json avec les versions



Table tous les paquets compilés
Name: string
Version tableau json avec les versions


## Links

* [Connect API Gateway with SQS](https://cloudhut.io/connect-aws-api-gateway-to-sqs-923cf312bf78)

* [EC2 Auto scaling from SQS metrics](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html)






## GANTT

### SPRINT 1
* **OLIVIER**
    * Create the squeleton of the architecture
* **JULIETTE**
    * Create a micro-service to search for packages
    * Create a micro-service to install packages
* **PIERRE**
    * Create client package manager architecture
    * Create local database and a microservice to update it
    * Create package manager command line interface

### SPRINT 2
* **OLIVIER** 
    * Implement the Lambda functions
    * Implement DynamoDB
    * Create the CRON TIMER to refresh the packages database and compile the needed
* **JULIETTE**
    * Create a micro-service to downgrade a package
    * Create a micro-service to upgrade a package
    * Create a micro-service to upgrade all packages
    * Create a micro-service to remove a package
* **PIERRE**
    * Link package manager interface to microservices
    * Manage user configuration
    * Optimize interface

### SPRINT 3
* **OLIVIER** 
    * Implement the auto-scaling of the EC2 instances
    * Adjust the Lambda function code, API Gateway and DynamoDB tables with the new requirements of the client
* **JULIETTE**
    * Create a web interface
* **PIERRE**
    * Add support for other package managers
    * Add functionnalities

### ROSETTA

* Request Amazon API Gateway


### Connection to a spot instance through the bastion server with local keys

```SHELL
ssh -i ~/Bureau/KeyPair_Server1.pem -o ProxyCommand='ssh -i ~/Bureau/KeyPair_Server1.pem -W %h:%p ubuntu@34.244.176.197' ubuntu@10.0.0.38
```

### Deploy the nested templates in CloudFormation

Put all the templates in S3 (main.yaml doesn't need it) and deploy main.yaml
It can be required to update the links in main.yaml to point to the S3 URL
