#! /bin/sh

# This script create the cron timer that execute the script that check if there is a package request
# The cron package used is sys-process/fcron


# Add the cron to the system's init process
/etc/init.d/fcron start
rc-update add fcron default

# Create a fcrontab file and add in the rules
touch /pacloud/fcrontab.cron
cat <<EOF >/pacloud/fcrontab.cron
SHELL=/bin/sh

# Not at boot, log only errors
!bootrun(false),nolog(true)
@ 10s /pacloud/AMI/script/cronJob.sh
EOF

# Enable the fcrontab
fcrontab /pacloud/fcrontab.cron


