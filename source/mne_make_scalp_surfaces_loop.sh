#!/bin/bash

for subject in SME{001..050};
do 
echo $subject
mne make_scalp_surfaces -s $subject -v -f
done
exit
