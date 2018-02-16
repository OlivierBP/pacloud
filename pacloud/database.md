# Databases comparison

## Arch Linux

Located in `/var/lib/pacman`
- local: contains folders for each installed packages. Each folder is [package name]-[version]
  - desc: contains informations on the package. %NAME%, %VERSION%, %DESC%, %DEPENDS% and stuff like that.
  - files: contains a list of the files to install %FILES%, and if it exists, %BACKUP%
  - mtree: gzip containing the files listed in `files`
- sync: contains gzip for each repo listed in `/etc/pacman.conf`. This is what is synchronized when using `pacman -Sy`. Every .db file contains a folder for each package containing the desc file described in the previous section.

## dpkg

Located in `/var/lib/dpkg`
- alternatives: folder containing files listing alternatives for packages (for example, awk lists nawk, gawk, mawk).
- available: List of available packages
- status: Status of available packages. Can be `install ok installed`.
- lock: a lock file to avoid running dpkg twice at the same time
- info: folder containing .list, .md5sums and hook scripts
  - .list: list of files regarding a package, similar to files in Arch
  - .md5sums: MD5 checksum for a package
  - .postinst: post installation script. Optional
  - .postrm, .preinst, .prerm: optional scripts.
- lots of other folders, seriously dpkg's DB is dirty.

## Gentoo

Located in `/usr/portage`  
Distributed in a tree of folders by categories: app-accessibility, app-admin...  
Each folder has a Manifest and metadata.xml files. Each leaf also has .ebuild(s) file(s).

## rpm

Located in `/var/lib/rpm`  
Uses Berkeley DB, a key/value NoSQL database.
