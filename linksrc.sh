#!/bin/bash
set -e
PROGDIR=$(dirname "$0") && cd "$PROGDIR"
mapfile -t lines < sources.conf
for source in "${lines[@]}"; do
    source=$(sed 's/^[[:blank:]]*//;s/[[:blank:]]*$//' <<< "$source")
    if [[ -z "$source" || $source =~ ^# ]]; then
        continue
    fi
    target=$(basename "$source")
    echo "[$source] -> [$target]"
    ln -svf --no-dereference "$source" "src/$target"
done
http://127.0.0.1:8000/mkdocs/CC%2B%2B/Modern%20C++.assets/image-20210212200114257.png