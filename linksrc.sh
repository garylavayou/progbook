#!/bin/bash

# scan sources
# for l in /mnt/d/Users/gary/Documents/程序设计/*; do
#   echo $(realpath $l); 
# done

set -e
PROGDIR=$(dirname "$0") && cd "$PROGDIR"
mapfile -t lines < sources.conf
for source in "${lines[@]}"; do
    # remove leading and trailing spaces for each line. 
    source=$(sed -E 's/#.+//;s/^[[:blank:]]*//;s/[[:blank:]]*$//' <<< "$source")
    if [[ -z "$source" || $source =~ ^# ]]; then
        continue
    fi
    target=$(basename "$source")
    echo "[$source] -> [$target]"
    ln -svf --no-dereference "$source" "src/$target"
done
