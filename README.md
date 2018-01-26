# GentooITT

## Context

This project is created by VARLEZ Pierre and BAL-PETRE Olivier for their 3rd year project at the IT Tallaght.

## Gentoo

> Gentoo Linux is a Linux distribution built using the Portage package management system. Unlike a binary software distribution, the source code is compiled locally according to the user's preferences and is often optimized for the specific type of computer. "Wikipedia"

## Problem

Take a lot of time to compile

Not important for a server but annoying for a desktop use.

Each time that a update is proposed for a software, need to recompile.

## Solution

Compile in the Cloud each package with a parameter file to compile for the desktop that need this package.

Advantages:
* Can use more powerful computers in the Cloud to compile faster.
* Don't use your resources when you can need it
* Compile the updates when a new appears and you just need to download them and install them
* Don't need to compile again the same package if you need it with the same parameters

## Our software

Command-line interface.
Download the binaries compiled in the Cloud and install them on the computer with Portage.

The server compile the package and store them in S3 with their parameter file. For each package, some informations about it are stored in a NO-SQL database (DynamoDB). These informations are:
* Name
* Versions
* Link to the S3 file
* Link to the parameter file
* Each parameter ??? (Could be nice to compare)

When a package is required by a client, the server check if it already compiled it with the same parameters. If yes, it can directly send to the client the binaries. If no, it will compile it. In this case, the client can choose to wait until the package is compiled ot to quit and let the package be compiled on the server and download it later. The client will get a notification that a package is ready to be download the next time that the command-line is used.

The server side will be highly available.
So we will have at least 2 EC2 instances running to compile the package when needed. If a lot of packages need to be compiled, it will automatically launch some other servers to handle the demand (horizontal auto-scaling).

AWS services used:
* EC2
* S3
* DynamoDB
* IAM
* CloudWatch
* CloudTrail
* SQS
* Route 53
* CloudFront
* CloudFormation to create the infrastructure and can manage it
* Maybe API Gateway
* Maybe Lambda
* Maybe SNS


TODO: Possibility to create a profil to have some list of package.

## Tasks

### Initial Project Proposal (28-Jan)

TODO
* Upload document with what is the project about
* create the group on Moodle with names, id...


### Detailed Project Proposal (5-Feb week)

### Research and Technology Review (19-Feb week)

### Exploration/Requirements (5-Mar week)

### Iteration 1 (19-Mar week)

### Iteration 2 (2-Apr week)

### Iteration 3 (16-Apr week)

### Presentation (23-Apr week)

## Bugs


## Resources

* [Readme Driven Development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)