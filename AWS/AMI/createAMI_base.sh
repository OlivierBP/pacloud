#! /bin/sh

# This script customize the AMI 
# Pygoscelis-Papua_Gentoo_HVM-2018-03-05-06-55-03 - ami-7d83c004
# that can be found in the community AMI

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

# Sync package database and update
emerge -uDU --keep-going --with-bdeps=y @world

# Install packages needed to work
emerge \
sys-process/htop \
app-misc/tmux \
app-text/tree \
app-misc/ranger \
dev-vcs/git 

# Install packages needed to to the job
emerge \
dev-python/pip \
app-misc/jq \
sys-process/fcron 


# install awscli with pip 
mkdir -p /pacloud
pip install awscli --user
mv /root/.local/bin/ /pacloud/

# Add awscli to the executables
ln -s /pacloud/bin/aws /bin/aws

# Configure the region for awscli
aws configure set region eu-west-1




# To be able to scp easily:
chown ec2-user:users /pacloud







