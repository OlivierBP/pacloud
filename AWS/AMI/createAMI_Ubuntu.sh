#! /bin/sh
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT
#
# Create the AMI for the Pacloud's workers from a Ubuntu AMI (tested with Ubuntu 16.04 LTS HVM)

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
docker.io \
hibagent

# Enable hibagent service
/usr/bin/enable-ec2-spot-hibernation

# Create /pacloud
mkdir -p /pacloud
# To be able to scp easily
chown ubuntu:users /pacloud


# DOCKER
docker pull olivierbp/pacloud
# !!!
# Another docker pull is made in the EC2 userdata to get the latest image

# CRONTAB
# Enable the service cron
systemctl enable cron
# Add the crontab instruction
echo "* * * * * root /pacloud/AMI/scripts/cronJob.sh >> /pacloud/crontab.log 2>&1" >> /etc/crontab

