#! /bin/sh

# Customize a Gentoo container to be a Pacloud worker

# To create from another container gentoo
#docker run -ti gentoo/stage3-x86 /bin/sh
#docker exec -ti containerIdOrName /bin/bash
#docker login --username olivierbp
#docker commit -a "olivierbp" -m "message" containerId olivier/pacloud:tags
#docker push olivierbp/pacloud:tags



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



# Sync
emerge -uDU --keep-going --with-bdeps=y @world

# Install packages needed to to the job
emerge \
dev-python/pip \
app-misc/jq \
sys-process/fcron 


# install awscli with pip 
mkdir -p /pacloud
pip install awscli --user
cp -r /root/.local/bin/ /pacloud/
# To be able to scp easily:
#chown ec2-user:users /pacloud

# Add awscli to the executables
ln -s /pacloud/bin/aws /bin/aws

# Configure the region for awscli
aws configure set region eu-west-1



# CRON
# Add the cron to the system's init process
#/etc/init.d/fcron start
#rc-update add fcron default

# Create a fcrontab file and add in the rules
#touch /pacloud/fcrontab.cron
#cat <<EOF >/pacloud/fcrontab.cron
#SHELL=/bin/sh

## Not at boot, log only errors
#!bootrun(false),nolog(true)
#@ 10s /pacloud/AMI/scripts/cronJob.sh
#EOF

# Enable the fcrontab
#fcrontab /pacloud/fcrontab.cron


