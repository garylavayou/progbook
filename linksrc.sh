#!/bin/bash
set -e
PROGDIR=$(dirname "$0") && cd "$PROGDIR"
while IFS=' ' read -r source target; do
    if [[ -z "$source" || $source =~ ^# ]]; then
        continue
    fi
    # echo "$source -> $target"
    ln -svf --no-dereference "$source" "src/$target"
done < sources.conf