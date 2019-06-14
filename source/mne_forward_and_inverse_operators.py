"""
Set up source space and compute forward and inverse operators.

To successfully run this script, following things need to be prepared:
    1) MRI preprocessing with Freesurfer
    2) coregistration with mne coreg
    3) noise covariance

Created on 9.8.2018
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
from datetime import datetime
import os.path
import numpy as np
import mne

#%matplotlib qt

# TO FILL
SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/' # MRI data
SUBJECTS = np.arange(1, 51)
SRCSPACING = "oct6" # source space setup
ICO_NTRI = 4 # Number of triangles in the BEM. Note that the Watershed
# algorithm always yields a 20480-triangle mesh which is here decimated by
# ICO_NTRI to give BEM_NTRI, e.g. 5=20484, 4=5120, 3=1280.
BEM_NTRI = 5120
MEG_DIR = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
preflood = 25 # for watershed algorithm
conductivity = [0.3]  # forward solution computation for one layer
mindist = 5.0 # for forward solution
loose = 0.2 # loose orientation constraint for inverse operator
depth = 0.8 # depth weighting for inverse operator
method = "MNE" # method to compute inverse solution

redo_BEM = 1 # Does the BEM need to be recalculated? 1 = yes, 0 = no
redo_inverse = 1 # Does the inverse operator need to be recalculated?

test = [1]
exclude = [17, 20, 29, 32, 40]
# exclusion reasons:
# SME018, SME021, SME030, SME041 no MRI, SME033 no MRI, no MEG
SUBJECTS = np.delete(SUBJECTS, exclude)

for subject in SUBJECTS:
#for subject in test:
    start_time = datetime.now()
    SUBJECT = 'SME' + '%03d' %subject
    MEG_SUBJECT = 'sme_' + '%03d' %subject
    CRGFILE = ('/media/cbru/SMEDY_SOURCES/DATA/MEG_prepro/' + MEG_SUBJECT
               + '/' + SUBJECT + '-trans.fif') # from coregistration
    COVFILE = MEG_DIR + '/emptyroom/empty_room_tsss-cov.fif' # noise covariance

    # these files will be created from this script
    SRCFILE = (SUBJECTS_DIR + '/'+ SUBJECT + '/bem/' + SUBJECT + '-'
               + SRCSPACING + '-src.fif')
    BEMFILE = (SUBJECTS_DIR + '/' + SUBJECT + '/bem/' + SUBJECT + '-'
               + str(BEM_NTRI) + '-bem.fif')
    SOLFILE = (SUBJECTS_DIR + '/' + SUBJECT + '/bem/' + SUBJECT + '-'
               + str(BEM_NTRI) + '-bem-sol.fif')

    if redo_BEM == 1:
        print('Calculating source space')
        # mne.bem.make_watershed_bem(SUBJECT, SUBJECTS_DIR, atlas=True,
        #                            preflood=preflood, show=False,
        #                            verbose=True, overwrite=True)
        # create BEM with watershed algorithm, this command does not work and
        # needs to be run manually with the command line given in
        # "Running subprocess: mri_watershed -h 25 ......."

        # Setup of Source Space
        src = mne.setup_source_space(SUBJECT, spacing=SRCSPACING,
                                     subjects_dir=SUBJECTS_DIR, add_dist=False)
        mne.viz.plot_bem(SUBJECT, SUBJECTS_DIR, src=src, show=True)
        text = input("Type in enter if the BEM is ok")
        if text == "":
            print(src)
            mne.write_source_spaces(SRCFILE, src, overwrite=True)
            # Compute the forward solution part 1 (MEG-data independent)
            model = mne.make_bem_model(subject=SUBJECT, ico=ICO_NTRI,
                                       conductivity=conductivity)
            mne.write_bem_surfaces(BEMFILE, model)
            bem = mne.make_bem_solution(model)
            mne.write_bem_solution(SOLFILE, bem)

    # find all _ssp files for this subject and do the following
    subject_folder = MEG_DIR + '/' + MEG_SUBJECT + '/'
    subject_files = os.listdir(subject_folder)

    for pieces in subject_files:
        if pieces[-8:] == '_ssp.fif': #find _ssp files
            final_path = subject_folder+pieces
            MEG_FILE = pieces
            MEG_SAVE = []
            if MEG_FILE[:4] == 'rest':
                MEG_SAVE = 'rest'
            elif MEG_FILE[:6] == 'speech':
                MEG_SAVE = 'speech'
            else:
                print('Something is wrong, your files are not named rest or speech')
            # these files will be created from this script
            FWDFILE = (MEG_DIR + '/' + MEG_SUBJECT + '/' + MEG_SAVE + '-'
                       + SRCSPACING + '-fwd.fif')
            INVFILE = (MEG_DIR + '/' + MEG_SUBJECT + '/' + MEG_SAVE + '-'
                       + SRCSPACING + '-meg-inv.fif')

            if redo_inverse == 1: #check
                print('Computing forward solution')
                print('--------------------------')
                # Compute the forward solution part 2 (MEG-data dependent)
                fwd = mne.make_forward_solution(MEG_DIR + MEG_SUBJECT + '/'
                                                + MEG_FILE, trans=CRGFILE,
                                                src=SRCFILE, bem=SOLFILE,
                                                meg=True, eeg=False,
                                                mindist=mindist, n_jobs=8)
                print(fwd)
                mne.write_forward_solution(FWDFILE, fwd, overwrite=True)

                # Compute the inverse operator
                print('Computing inverse operator')
                print('--------------------------')
                # Read the forward solution and compute the inverse operator
                fwd = mne.read_forward_solution(FWDFILE)
                fwd = mne.pick_types_forward(fwd, meg=True, eeg=False)

                # make an MEG inverse operator
                # needs to be changes to something without baseline
                raw = mne.io.read_raw_fif(final_path, preload=False)
                info = raw.info
                noise_cov = mne.read_cov(COVFILE)
                inv_op = mne.minimum_norm.make_inverse_operator(info, fwd,
                                                                noise_cov,
                                                                loose=loose,
                                                                depth=depth)
                del fwd
                mne.minimum_norm.write_inverse_operator(INVFILE, inv_op)

    end_time = datetime.now()
    print('The processing for subject ' + SUBJECT + ' took: {}'.format(end_time - start_time))
