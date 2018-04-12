#! /bin/bash
#
# Project Pacloud https://github.com/OlivierBP/Pacloud
# Created by BAL-PETRE Olivier
# License MIT 
#
# This script parse the DB of files got by:
# git clone https://github.com/gentoo-mirror/gentoo

DynamoDbTable=test2

batchItem="{\"$DynamoDbTable\": ["
nbItemBatch=0

nbTotalPackages=0

cd $1
# Foreach parent folder
for dir in $(ls -d */); do
    cd $dir
    
    # Foreach package
    for pac in $(ls -d */); do
        cd $pac

        # Remove the letter "/" at the end
        pac=${pac::-1}
            
        for fil in $(ls *.ebuild); do
            version=$(echo $fil | sed "s/$pac-//" | sed "s/\.ebuild//")
            
            item="{ \
                        \"PutRequest\": { \
                            \"Item\": { \
                                \"name\": { \
                                    \"S\": \"$dir$pac\" \
                                }, \
                                \"version\": { \
                                    \"S\": \"$version\" \
                                } \
                            } \
                        } \
                    },"
            #aws dynamodb put-item --table-name $DynamoDbTable --item "$item" &
            ((nbTotalPackages++))
            echo $nbTotalPackages
            # Batch processing
            batchItem+=$item
            ((nbItemBatch++))
            if [ $nbItemBatch -eq 25 ]; then
                batchItem=${batchItem::-1}
                batchItem+="] }"
                aws dynamodb batch-write-item --request-items "$batchItem" 
                batchItem="{\"$DynamoDbTable\": ["
                nbItemBatch=0
            fi

        done

        cd ..
    done

    cd ..
done

# Upload the last batch item
batchItem=${batchItem::-1}
batchItem+="] }"
aws dynamodb batch-write-item --request-items "$batchItem"

echo "Job done !!"
