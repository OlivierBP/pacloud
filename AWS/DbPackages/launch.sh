#!/bin/bash



for d in $(ls -d *); do
  echo $d
  ./.convertdb.sh $d
done
