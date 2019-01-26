# Create the file packages DB


Being in `pacloud/AWS/DbPackages/`.

```BASH
# Clone the Gentoo's repository
git clone https://github.com/gentoo-mirror/gentoo
cd gentoo

# Copy the scripts
cp ../convertdb.sh .convertdb.sh
cp ../launch.sh .launch.sh

# Exec the script
./.launch.sh

# Put all the files in a directory
mkdir -p db-files
mv *.json db-files

# Create the manifest
ls -d */ | sed 's/\/\s*//g' > manifest.txt
mv manifest.txt db-files/
```

All the files in `db-files` must now be uploaded in S3 at `https://s3-eu-west-1.amazonaws.com/pacloud-packages-bucket/db-files/` **and** must be set public.
