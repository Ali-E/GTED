tag1=$(basename $1 | cut -d"." -f1)
tag2=$(basename $2 | cut -d"." -f1)
k=$3
echo $tag1 $tag2 $k

/s/chopin/a/grad/akashsht/devel/hyda/bin/import -f=$1 -f=$2 -O=dump/reads.fasta
/s/chopin/a/grad/akashsht/devel/hyda/bin/assemble-unitig -O=dump/$tag1-$tag2-$k -C=twocolor.config -k=$k -S dump/reads.fasta
/s/chopin/a/grad/akashsht/devel/hyda/bin/assemble-finish -U=dump/$tag1-$tag2-$k.unitigs -O=dump/$tag1-$tag2-$k -c=0 -S -a dump/reads.fasta
/s/chopin/a/grad/akashsht/devel/hyda/bin/asmtogted -A=dump/$tag1-$tag2-$k.asm -O=dump/$tag1-$tag2-$k
rm -f dump/$tag1-$tag2-$k.asm dump/$tag1-$tag2-$k.extcontigs dump/$tag1-$tag2-$k.contigs dump/$tag1-$tag2-$k.unitigs
