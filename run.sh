#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root=$DIR

cd $root
echo "Updating data..."
doit convert convert_index merge merge_index adjusted_close book2market 

echo "Copying data to master..."
cp -ruv $root/merged/* $root/master/

echo "Running transformation tasks..."
doit monthly_avg_momentum pead_momentum