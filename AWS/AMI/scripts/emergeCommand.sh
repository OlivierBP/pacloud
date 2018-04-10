#! /bin/sh

package=$1
version=$2

emerge --buildpkgonly =$package-$version

