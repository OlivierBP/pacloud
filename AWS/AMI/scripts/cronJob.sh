#! /bin/sh

# Script started regularly by a cron job
# Check if something is compiling and if there is a compilation request. Start a compilation if needed

# Check if there is a lock

    # Put a lock

    #try
    # Call the compilation script
    /pacloud/AMI/scripts/compilationPackage.sh
    #fin try

    # Release the lock (if the job fail ?




