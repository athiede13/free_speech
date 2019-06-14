#!/bin/sh
#
# Batch script for maxfiltering a number of files
#
# Author: Lauri Parkkonen <lauri@neuro.hut.fi>
# modified for free_speech project by Anja Thiede <anja.thiede@helsinki.fi>

if [ $# -lt 1 ]
then
  echo "Usage: bash $0 <infile1> [<infile2> ...]"
  exit 1
fi

infiles=$*

prog="maxfilter-2.2"
args="-autobad 60 -origin 0 0 40 -frame head -movecomp inter -hpicons -st -site biomag_triux -v"
suff="_tsss_mc"

echo "About to run MaxFilter on $infiles"
#echo "Press <enter> to continue"
#read a

basepath="/l/thiedea1/MEG_speech_rest_orig/"

for f in $infiles
do
  barefile=`basename $f .fif`
  abspath=`dirname $f`
  echo "Found abspath $abspath"
  relpath=${abspath##$basepath}
  echo "and relpath $relpath"
  outpath="/l/thiedea1/MEG_prepro/"$relpath
  echo "and outpath $outpath"
  mkdir -p $outpath
  outfile=$outpath/${barefile::-8}$suff".fif"
  logfile=$outpath/${barefile::-8}$suff".log"
  echo "----------------------------------------"
  echo "Processing $f --> $outfile"
  $prog $args -f $f -o $outfile > $logfile
done
echo "[done]"
exit $?
