#! /bin/sh

# Script started regularly by a cron job
# Check if something is compiling and if there is a compilation request. Start a compilation if needed

# Check if there is a lock
if [ ! -d "/pacloud/compiling.lock" ]; then

    # Put a lock
    mkdir /pacloud/compiling.lock

    { # try
        # Call the compilation script
        #/pacloud/AMI/scripts/compilePackage.sh
        docker run --rm --cap-add=SYS_PTRACE olivierbp/pacloud:version4 /pacloud/AMI/scripts/compilePackage.sh
    } || { # catch
        echo "compilation script failed"
    }
    
    # Release the lock
    rm -r /pacloud/compiling.lock
fi

