#!/bin/sh
# In order to deploy the build, I need to filter out files that is not desired for 
# publish.
# 
# Related issues:
#  - https://github.com/rust-lang/mdBook/issues/1187
#  - https://github.com/rust-lang/mdBook/pull/1908

set -e
# MODE='ugo+r,u+w,go-w,Fugo-x'
PROGDIR=$(dirname "$0") && cd "$PROGDIR"
MODE='F644,D755'
DATE=$(date +'%Y%m%d')
# MODE='u=rw,go=r,D+x'
src=mdbook

rsync -uav --delete --exclude-from='.rsync-ignore' \
      --chmod=$MODE \
      book/* /tmp/progbook-$src/

# rsync -uav --delete --exclude-from='.rsync-ignore' \
#       --chmod=$MODE \
#       site/* /tmp/progbook-mkdocs/
dir=$(pwd)

ln -svf --no-dereference "/tmp/progbook-$src" "/tmp/progbook-$src-$DATE"
tar -czvf "$dir/progbook-$src-$DATE.tar.gz" -C /tmp --dereference "progbook-$src-$DATE"
ls -lh "$dir/progbook-$src-$DATE.tar.gz"
# +X: add executability (not consistent with chmod +X)
# rsync -uav --delete $WORKDIR/progbook-mdbook/* \
#       --exclude='README.md' \
#       $dir/../garylavayou.github.io/