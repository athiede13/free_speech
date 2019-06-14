"""
Morph source data from an individual subject to freesurfer's fsaverage brain.

Created on Wed Aug 15 11:09:31 2018
Updated on 2.5.2019 with new function mne.compute_source_morph
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
from datetime import datetime
import os.path
import fnmatch
import numpy as np
import mne

now = datetime.now()

# FILL
MEG_DIR = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/' # MRI data
SUBJECTS = np.arange(1, 51)
exclude = [17, 20, 22, 29, 32, 40]
# exclusion reasons:
# SME018, SME021, SME030, SME041 no MRI, SME033 no MRI, no MEG
# no trigger codes for SME023
SUBJECTS = np.delete(SUBJECTS, exclude)

test = [1]

log_path = MEG_DIR+'logs/morph_to_fsaverage_'+now.strftime("%Y-%m-%d")+'.log'
log = open(log_path, 'w')

check_existing_morphs = 1 # 0=no, means will redo morphing, 1=yes, won't redo,
# if morph already exists
# END FILL

for subject in SUBJECTS:
#for subject in test:
    start_time = datetime.now()
    SUBJECT = 'SME' + '%03d' %subject
    MEG_SUBJECT = 'sme_' + '%03d' %subject
    subject_folder = MEG_DIR + '/' + MEG_SUBJECT + '/'
    subject_files = os.listdir(subject_folder)

    for stc_fname in fnmatch.filter(subject_files, 'sme*energy*_21-lh.stc'):
        final_path = subject_folder+stc_fname
        MORPHEDFILE = subject_folder + stc_fname[:-7] + '_MNE'

        if check_existing_morphs == 1:
            if not os.path.isfile(MORPHEDFILE + '-lh.stc'):
                print('Morphing file: ' + stc_fname)
                print('--------------------------------------------------')
                # Load stc to in common cortical space (fsaverage)
                stc_from = mne.read_source_estimate(final_path)
                # Morph data to average brain
                morph = mne.compute_source_morph(stc_from, subject_from=SUBJECT,
                                                 subject_to='fsaverage',
                                                 subjects_dir=SUBJECTS_DIR,
                                                 spacing=5, smooth=None,
                                                 warn=True, verbose=True)
                stc_fsaverage = morph.apply(stc_from)
                # save
                stc_fsaverage.save(MORPHEDFILE, ftype='stc', verbose=True)
                log.write(MORPHEDFILE+' done\n')
            else:
                print(MORPHEDFILE + ' already morphed')
                log.write(MORPHEDFILE+' exists already\n')
        else:
            print('Morphing file: ' + stc_fname)
            print('--------------------------------------------------')
            # Load stc to in common cortical space (fsaverage)
            stc_from = mne.read_source_estimate(final_path)
            # Morph data to average brain
            morph = mne.compute_source_morph(stc_from, subject_from=SUBJECT,
                                             subject_to='fsaverage',
                                             subjects_dir=SUBJECTS_DIR,
                                             spacing=5, smooth=None, warn=True,
                                             verbose=True)
            stc_fsaverage = morph.apply(stc_from)
            # save
            stc_fsaverage.save(MORPHEDFILE, ftype='stc', verbose=True)
            log.write(MORPHEDFILE+' done\n')

    end_time = datetime.now()
    print('The processing for subject ' + SUBJECT + ' took: {}'.format(end_time - start_time))

print('done')
log.close()
