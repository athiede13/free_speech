#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Assign bad channels in MNE.

Created on Thu Nov  2 17:13:35 2017
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
import os
import os.path as op
import mne

# find file paths and correct files
file_path = ('/media/cbru/SMEDY_DATA/SMeDy_DATA/MEG_orig_all/')
subject = ('sme_001/')
fname = ('tata_a_raw.fif')
#fname = ('tata_a_raw-1.fif')
os.chdir(op.join(file_path, subject))
# the date_folder is different for every subject, that is why we need this
# detour to access the file
date_folder = [name for name in os.listdir('.') if os.path.isdir(name)]

# load data
raw = mne.io.read_raw_fif(op.join(file_path, subject, date_folder[1], fname))
raw.plot(order='type', lowpass=80, highpass=.58, remove_dc=True)

# assign bad channels
raw.info['bads'] = [u'MEG0342', u'MEG1013', u'MEG1623', u'MEG1633', u'MEG2422',
                    u'MEG2023']  # mark bad channels
# raw.info['bads'] # just to check whether the assignment was successful

# save
out_fname = fname[:-7]+'bad_raw.fif'
#out_fname = fname[:-9]+'bad_raw.fif'
out_folder = op.join(file_path, subject)
raw.save(op.join(out_folder, out_fname))
