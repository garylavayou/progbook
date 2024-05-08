#!/bin/bash -e

# get necessary fonts data required by css files.

THEME_DIR=${THEME_DIR:-'docs/docsify-themes'}
DOCSIFY_DIR=${DOCSIFY_DIR:-'docs/docsify-plugins/node_modules/docsify'}
TARGET_DIR=${TARGET_DIR:-'docs'}

if [ ! -e "$DOCSIFY_DIR" ]; then
    cwd=$(pwd)
    # shellcheck disable=SC2046
    cd $(dirname $(dirname "$DOCSIFY_DIR"))
    npm install
    cd "$cwd"
fi
rsync -uav "$DOCSIFY_DIR/themes/" "$THEME_DIR/"

mkdir -p "${THEME_DIR}/fonts"
for css in "$THEME_DIR"/*.css; do
    echo "$css"
    url=$(sed -En 's/@import\s*url\("(.*)"\);/\1/p' <"$css")
    if [ -z "$url" ]; then
        if [[ $(basename -s .css "$css") =~ pure ]]; then
           /bin/cp -vf "$css" "${THEME_DIR}/fonts/$(basename $css)" 
        fi
    else
        css=$(basename "$css")
        # css_name=$(sed -E 's/(.*).css/\1/' <<< "$css")
        wget -v \
             --output-document="${THEME_DIR}/fonts/$css" \
             "$url"
    fi
done

for css in "$THEME_DIR"/fonts/*.css; do
    echo "$css"
    font_info=$(grep -oE 'url(\((.*)\))\s' < "${css}" | sed -E 's/url\((.*)\)/\1/')
    readarray -t fonts <<< "$font_info"
    for url in "${fonts[@]}"; do
        echo "$url"
        fontpath=$(sed -E 's/https?:\/\/(.*\.com)\/(.+)/\2/' <<<"$url")
        fontdir=$(dirname "$fontpath")
        # --input-file=-
        wget \
            --directory-prefix="${TARGET_DIR}/docsify-fonts/${fontdir}" \
            --timestamping \
            "$url"
    done
done