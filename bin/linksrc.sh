#!/bin/bash

function usage(){
    echo "usage: link folders containing source files into the workspace."
    echo "syntax: ./bin/linksrc.sh [TARGET]"
    echo ""
    echo "arguments:"
    echo "  TARGET: where to put the linked source file target (default: src)"
    echo ""
    echo "notes:"
    echo "  folders that need to be linked are specified in 'sources.conf' in "
    echo "  current working folder."
    exit 1
}

SOURCE_DIR=${SOURCE_DIR:-'src'}

set -e
# PROGDIR=$(dirname "$0")
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi
mapfile -t lines < sources.conf
mkdir -p "${SOURCE_DIR}"
for source in "${lines[@]}"; do
    # remove leading and trailing spaces for each line. 
    source=$(sed -E 's/#.+//;s/^[[:blank:]]*//;s/[[:blank:]]*$//' <<< "$source")
    if [[ -z "$source" || $source =~ ^# ]]; then
        continue
    fi
    target=$(basename "$source")
    ln -svf --no-dereference "$source" "${SOURCE_DIR}/$target"
done
