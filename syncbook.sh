#!/bin/sh
set -e
# MODE='ugo+r,u+w,go-w,Fugo-x'
PROGDIR=$(dirname "$0") && cd "$PROGDIR"
MODE='F644,D755'
DATE=$(date +'%Y%m%d')
# MODE='u=rw,go=r,D+x'

rsync -uav --delete --exclude-from='.rsync-ignore' \
      --chmod=$MODE \
      book/* /tmp/progbook-mdbook/
rsync -uav --delete --exclude-from='.rsync-ignore' \
      --chmod=$MODE \
      site/* /tmp/progbook-mkdocs/

dir=$(pwd)

for src in 'mdbook' 'mkdocs'; do
     tar -czf $dir/progbook-$src-$DATE.tar.gz -C /tmp progbook-$src
done

# +X: add executability (not consistent with chmod +X)
