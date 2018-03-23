#! /bin/sh

# Send the AMI directory to a EC2 machine through the bastion server


bastionUser=ubuntu
bastionIp=52.51.219.136

workerUser=ec2-user
workerIp=10.0.2.177


cmd="scp -i ~/Bureau/KeyPair_Server1.pem -o ProxyCommand='ssh -i ~/Bureau/KeyPair_Server1.pem -W %h:%p $bastionUser@$bastionIp' -r /home/olivier/PROJECTS/Pacloud/AWS/AMI/ $workerUser@$workerIp:/home/ec2-user/"

eval $cmd

