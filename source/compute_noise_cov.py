"""
Computation of noise covariance from empty-room MEG data.

Created on 9.8.2018
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

# set up environment
import os.path as op
import mne

# set up data paths
root_path = ('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/')
# read in emptyroom data (preprocessed)
raw_empty_room_fname = op.join(root_path, 'emptyroom/empty_room_tsss.fif')
raw_empty_room = mne.io.read_raw_fif(raw_empty_room_fname)
# compute noise covariance
noise_cov = mne.compute_raw_covariance(raw_empty_room, tmin=0, tmax=None)
# plot
noise_cov.plot(raw_empty_room.info, proj=True)
fig_cov, fig_spectra = mne.viz.plot_cov(noise_cov, raw_empty_room.info)
# save
fsave = raw_empty_room_fname[:-4]+'-cov.fif'
print(fsave)
noise_cov.save(fsave)
del noise_cov
