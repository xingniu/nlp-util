#!/bin/bash

# Extract non-audio files and repack them.
# Usage: MSLP-repack.sh </absolute/path/to/MSLT_Corpus.zip>

tmpdir=`mktemp -d`
unzip "$1" -d $tmpdir -x *.wav
tgzfile=$(echo "$1" | rev | cut -d. -f2- | rev).tgz
cd $tmpdir
tar -cvzf $tgzfile *
rm -rf $tmpdir
echo "Converted $1 to $tgzfile"
