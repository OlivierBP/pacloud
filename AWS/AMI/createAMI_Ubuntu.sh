#! /bin/sh

# Create the AMI for the Pacloud's workers from a Ubuntu AMi (tested with Ubuntu 16.04 LTS HVM

# Update
apt-get update

# Install packages needed to work
apt-get --assume-yes install \
tree \
htop \
ranger \
git \
tmux

# Install the packages needed to do the job
apt-get --assume-yes install \
jq \
cron \
awscli \
hibagent \
gcc \
tar 

# Enable hibagent service
/usr/bin/enable-ec2-spot-hibernation

# Configure the region for awscli
aws configure set region eu-west-1

# Create /pacloud
mkdir -p /pacloud
# To be able to scp easily
chown ubuntu:users /pacloud



# DOCKER
# docker ps --all
apt install docker.io

# To create from another container gentoo
#docker run -ti plabedan/gentoo-minimal /bin/sh
#docker exec -ti containerIdOrName /bin/bash








# PORTAGE
wget https://codeload.github.com/gentoo/portage/tar.gz/repoman-2.3.28 -O /pacloud/portage-2.3.28.tar.gz 
tar --extract --gz --verbose --file /pacloud/portage-2.3.28.tar.gz -C /pacloud/
cd /pacloud/portage-repoman-2.3.28
python setup.py install
echo "portage:x:250:250:portage:/var/tmp/portage:/bin/false" >> /etc/passwd
echo "portage::250:portage" >> /etc/group
mkdir -p /usr/portage
# Sync packages database
emerge --sync
# Link a profile
ln -s ../../usr/portage/profiles/default/linux/amd64/17.0/no-multilib /etc/portage/make.profile

# Get the number of core
nbcore=$(nproc --all)

# Set flags in /etc/portage/make.conf
# MAKEOPTS number of parallel make jobs that can be used for a single package build (Should be equal to the number of cores on the machine)
# EMERGE_DEFAULT_OPTS --job Enable N parallel package build --load-average set to N*1.0 to have 100%
cat <<EOF >/etc/portage/make.conf
CFLAGS="-O2 -pipe"
CHOST="x86_64-pc-linux-gnu"
USE="mmx sse sse2 static-libs"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j$nbcore"
EMERGE_DEFAULT_OPTS="--jobs=1 --load-average=1.0"
EOF

#apt install automake
#apt install build-essential
#emerge --oneshot sys-apps/portage














# CRONTAB
# Enable the service cron
systemctl enable cron

# Add the crontab instruction
echo "* * * * * root /pacloud/AMI/scripts/cronJob.sh" >> /etc/crontab



