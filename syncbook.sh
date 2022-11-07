# MODE='ugo+r,u+w,go-w,Fugo-x'
PROGDIR=$(realpath $(dirname syncbook.sh))
MODE='F644,D755'
DATE=$(date +'%Y%m%d')
# MODE='u=rw,go=r,D+x'

cd $PROGDIR
rsync -uav --delete --exclude-from='.rsync-ignore' \
      --chmod=$MODE \
      book/* /home/gary/downloads/progbook-mdbook/
rsync -uav --delete --exclude-from='.rsync-ignore' \
      --chmod=$MODE \
      site/* /home/gary/downloads/progbook-mkdocs/

dir=$(pwd)
cd /home/gary/downloads/

for src in 'mdbook' 'mkdocs'; do
     tar -cf $dir/progbook-$src-$DATE.tar progbook-$src
done

# +X: add executability (not consistent with chmod +X)
