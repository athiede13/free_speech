# -*- coding: utf-8 -*-
"""
EOG channel assignment/fix.
- read all preprocessed files
- check whether EOG channels are correctly assigned
- fix EOG assignment if not
- save with '_EOG' extension

Created on Mon Jan  8 15:55:09 2018
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
import os
from os import walk
import datetime
import mne

now = datetime.datetime.now()

#test= ['sme_049'] # subjects with weird EOG channels

root_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
log_path = root_path+'EOG_fix_'+now.strftime("%Y-%m-%d")+'.log'
log = open(log_path, 'w')

f = []
for (dirpath, dirnames, filenames) in walk(root_path):
    f.extend(filenames)
    break

exclude = []
for i in range(0, len(exclude)):
    dirnames.remove(exclude[i])

#for subject in test:
for subject in dirnames:
    subject_folder = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'+subject+'/'
    subject_files = os.listdir(subject_folder)
    for pieces in subject_files:
        if pieces[-11:] == 'tsss_mc.fif':
            final_path = subject_folder+pieces
            print(final_path)
            raw = mne.io.read_raw_fif(final_path, preload=False) # read preprocessed data
            #print(raw.info)
            print(raw.info['ch_names'][0:2]) # are both EOG channels here?
            if raw.info['ch_names'][0:2] == [u'EOG001', u'EOG002']:
                print('everything cool with subject ', subject)
                log.write(subject+ ' ' + pieces +' EOG ok\n')
            elif os.path.isfile(subject_folder+pieces[:-4]+'_EOG.fif'):
                print('this has been fixed already ', subject)
                log.write(subject+ ' ' + pieces +' has been fixed\n')
            else:
                print('better check EOGs of subject ', subject)
                log.write(subject+ ' ' + pieces +' check EOG\n')
                log.write(str(raw.info['ch_names'][0:2])+'\n')
                # the following two lines are only relevant, if the EOG
                # channels were not mapped correctly
                raw.set_channel_types({'BIO003' : 'eog'})
                mne.rename_channels(raw.info, {u'BIO003' : u'EOG002'})
                #print(raw.info)
                print(raw.info['ch_names'][0:2]) # are both EOG channels here?
                root, ext = os.path.splitext(final_path)
                raw.save(root+'_EOG'+ext)
                print('[done]')
                log.write('[done]\n')

log.close()
