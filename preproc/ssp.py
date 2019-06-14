"""
Removal of eye blink and heart beat artifacts by signal space projection (SSP).

Created on 31.10.2017
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
import os
from os import walk
import datetime
import mne
from mne.preprocessing import compute_proj_eog
from mne.preprocessing import compute_proj_ecg

now = datetime.datetime.now()

def processedcount(file_list):
    """Counts to how many files SSP has already been added to."""
    n = 0
    for item in file_list:
        if item[-7:-4] == 'ssp':
            n = n+1
    return n

root_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'

f = []
for (dirpath, dirnames, filenames) in walk(root_path):
    f.extend(filenames)
    break

reject = dict(grad=3000e-13, # T / m (gradiometers)
              mag=5000e-15, # T (magnetometers)
              eeg=100, # uV (EEG channels)
              )

log_path = root_path+'logs/ssp2_'+now.strftime("%Y-%m-%d")+'_summary.log'
log = open(log_path, 'w')

exclude = []#['sme_015', 'sme_021']
for i in range(0, len(exclude)):
    dirnames.remove(exclude[i])

# first loop for the EOG-fixed files
for subject in dirnames:
    subject_folder = root_path+subject+'/'
    subject_files = os.listdir(subject_folder)
    ssp_file_count = processedcount(subject_files)
    # if both (speech and rest) _ssp.fif exist already in subjects folder,
    # then don't process the subject again
    if ssp_file_count == 2:
        continue
    for pieces in subject_files:
        if pieces[-15:] == 'tsss_mc_EOG.fif':
            final_path = subject_folder+pieces
            print(final_path)
            raw = mne.io.read_raw_fif(final_path, preload=True)
            projection_ecg, ecg_events = compute_proj_ecg(raw, reject=reject,
                                                          l_freq=1, h_freq=100,
                                                          tstart=5,
                                                          ecg_h_freq=25,
                                                          ecg_l_freq=1,
                                                          average=True,
                                                          ch_name='MEG1541')
            projection_eog, eog_events = compute_proj_eog(raw, reject=reject,
                                                          l_freq=1, h_freq=40,
                                                          average=True)
            raw_ecg_removed = raw.add_proj(projection_ecg, remove_existing=True)
            raw_all_removed = raw_ecg_removed.add_proj(projection_eog)
            save_path = subject_folder+pieces[:-4]+'_ssp.fif'
            print(save_path)
            raw_all_removed.apply_proj().save(save_path, overwrite=True)
            del projection_ecg, ecg_events, projection_eog, eog_events
            del raw_ecg_removed, raw_all_removed
            log.write(subject+' processed\n')

# second loop for the rest
for subject in dirnames:
    subject_folder = root_path+subject+'/'
    subject_files = os.listdir(subject_folder)
    ssp_file_count = processedcount(subject_files)
    if ssp_file_count == 2: #check again
        continue
    for pieces in subject_files:
        if pieces[-11:] == 'tsss_mc.fif':
            final_path = subject_folder+pieces
            print(final_path)
            raw = mne.io.read_raw_fif(final_path, preload=True)
            projection_ecg, ecg_events = compute_proj_ecg(raw, reject=reject,
                                                          l_freq=1, h_freq=100,
                                                          tstart=5,
                                                          ecg_h_freq=25,
                                                          ecg_l_freq=1,
                                                          average=True,
                                                          ch_name='MEG1541')
            projection_eog, eog_events = compute_proj_eog(raw, reject=reject,
                                                          l_freq=1, h_freq=40,
                                                          average=True)
            raw_ecg_removed = raw.add_proj(projection_ecg, remove_existing=True)
            raw_all_removed = raw_ecg_removed.add_proj(projection_eog)
            save_path = subject_folder+pieces[:-4]+'_ssp.fif'
            print(save_path)
            raw_all_removed.apply_proj().save(save_path, overwrite=True)
            del projection_ecg, ecg_events, projection_eog, eog_events
            del raw_ecg_removed, raw_all_removed
            log.write(subject+' processed\n')

log.close()
