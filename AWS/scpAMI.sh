#! /bin/sh
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT 
#
# Send the AMI directory to a EC2 machine through the bastion server


bastionUser=ubuntu
bastionIp=34.242.1.193

workerUser=ec2-user
workerIp=10.0.4.133


cmd="scp -i ~/Bureau/KeyPair_Server1.pem -o ProxyCommand='ssh -i ~/Bureau/KeyPair_Server1.pem -W %h:%p $bastionUser@$bastionIp' -r /home/olivier/PROJECTS/Pacloud/AWS/AMI/ $workerUser@$workerIp:/pacloud/"

eval $cmd

