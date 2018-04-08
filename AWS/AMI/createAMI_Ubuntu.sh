#! /bin/sh

# Create the AMI for the Pacloud's workers from a Ubuntu AMI (tested with Ubuntu 16.04 LTS HVM

# Update
apt-get --assume-yes update

# Install packages needed to work
apt-get --assume-yes install \
tree \
htop \
ranger \
git \
tmux

# Install the packages needed to do the job
apt-get --assume-yes install \
#jq \
#cron \
#awscli \
hibagent \
#gcc \
#tar 

# Enable hibagent service
/usr/bin/enable-ec2-spot-hibernation

# Configure the region for awscli
#aws configure set region eu-west-1

# Create /pacloud
mkdir -p /pacloud
# To be able to scp easily
chown ubuntu:users /pacloud




# DOCKER
# docker ps --all
apt assume-yes install docker.io

#docker run -ti --cap-add=SYS_PTRACE olivierbp/pacloud:version1 /bin/bash &





# CRONTAB
# Enable the service cron
systemctl enable cron

# Add the crontab instruction
echo "* * * * * root /pacloud/AMI/scripts/cronJob.sh >> /pacloud/crontab.log 2>&1" >> /etc/crontab
