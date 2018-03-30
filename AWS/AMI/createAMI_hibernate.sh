#! /bin/sh



##################################
# After that: test

# Rebuild the kernel (TODO: Set directly a .config file to build the kernel)
cd /usr/src/linux/
make menuconfig
# In the TUI opened:
# "Power management and ACPI options" ---> enable "Hibernation (aka 'suspend to disk')"
# Save
# Ok
make


# Install hibagent to be able to hibernate on the spotfleet commands
git clone https://github.com/aws/ec2-hibernate-linux-agent /pacloud/hibagent
cd /pacloud/hibagent/
python setup.py install



# In /usr/bin/enable-ec2-spot-hibernation
# replace /sbin/chkconfig hibagent on
# with rc-update add hibagent default
# replace exec service hibagent start
# with hibagent





# Remove grub legacy and replace with grub
emerge --depclean grub-static
emerge sys-boot/grub
grub-mkconfig -o /boot/grub/grub.cfg


sys-power/pm-utils
sys-power/suspend
sys-power/hibernate-script

