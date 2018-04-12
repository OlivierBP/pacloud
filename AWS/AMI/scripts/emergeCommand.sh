#! /bin/sh
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT 
#
# This script contains the command to merge the requested package

package=$1
version=$2
useflag=$3


# Build all the build time dependencies (not the run time dependencies) then build the binary for the requested package
env USE="$useflag" \
    emerge \
    --onlydeps \
    --onlydeps-with-rdeps n \
    =$package-$version \
    && emerge --buildpkgonly =$package-$version


#env USE="-X -gnome" emerge mc
#USE="uci" emerge --pretend --onlydeps -- onlydeps-with-rdeps n p7zip
