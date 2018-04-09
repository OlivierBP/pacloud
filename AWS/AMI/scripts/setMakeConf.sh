#! /bin/sh

# Set flags in /etc/portage/make.conf

# Get the number of core
nbcore=$(nproc --all)

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

