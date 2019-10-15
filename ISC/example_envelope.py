"""
Plot amplitude envelopes of example subjects

Created on Thu Sep 12 08:57:20 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import matplotlib.pyplot as plt
import numpy as np
import mne
import wave
import sys

#%matplotlib qt
#%matplotlib inline

path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
subject1 = 'sme_012'
subject2 = 'sme_035'
subject3 = 'sme_011' # dys
subject4 = 'sme_024' # dys
fre = '12-25Hz'
con = '_10'
source = 2459 # source point with largest difference between groups
sf = 3146/287
# audio file
speech_file = '/media/cbru/SMEDY_SOURCES/stimuli/presentation_final/speech/stimuli/speech_part1.wav'

final_path1 = path + subject1 + '/' + subject1 + '_energy_' + fre + con + '_MNE-lh.stc'
final_path2 = path + subject2 + '/' + subject2 + '_energy_' + fre + con + '_MNE-lh.stc'
final_path3 = path + subject3 + '/' + subject3 + '_energy_' + fre + con + '_MNE-lh.stc'
final_path4 = path + subject4 + '/' + subject4 + '_energy_' + fre + con + '_MNE-lh.stc'

stc1 = mne.read_source_estimate(final_path1)
stc2 = mne.read_source_estimate(final_path2)
stc3 = mne.read_source_estimate(final_path3)
stc4 = mne.read_source_estimate(final_path4)

# prepare the envelope time courses plots at a specific source point

t_start = round(250*sf)
t_length = 220 #20*sf
#t_start = 0
#t_length = 3146
y = stc1.data[source, t_start:t_start+t_length]
x = stc1.times[t_start:t_start+t_length]/sf
y2 = stc2.data[source, t_start:t_start+t_length]
x2 = stc2.times[t_start:t_start+t_length]/sf
y3 = stc3.data[source, t_start:t_start+t_length]
x3 = stc3.times[t_start:t_start+t_length]/sf
y4 = stc4.data[source, t_start:t_start+t_length]
x4 = stc4.times[t_start:t_start+t_length]/sf

# prepare the wave sound file plots
with wave.open(speech_file,'r') as wav_file:
    #Extract Raw Audio from Wav File
    signal = wav_file.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    #Split the data into channels 
    channels = [[] for channel in range(wav_file.getnchannels())]
    for index, datum in enumerate(signal):
        channels[index%len(channels)].append(datum)

    #Get time from indices
    fs = wav_file.getframerate()
    t1 = 250*fs
    t2 = 270*fs
    Time=np.linspace(0, len(signal)/len(channels)/fs, num=len(signal)/len(channels))
    
#%% plot subplots    
# all font size settings
SMALL_SIZE = 15
MEDIUM_SIZE = 17
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=False, figsize = (12,12))
# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.3)
ax1.plot(x, y, x2, y2)
ax1.set(ylabel='envelope amplitude',
        title='2 example control participants with low ISC (r=0.07)',
        ylim=(0.7, 1.5))
#ax1.grid()

ax2.plot(x3, y3, x4, y4)
ax2.set(ylabel='envelope amplitude',
       title='2 example dyslexic participants with high ISC (r=0.46)',
       yticks=np.arange(0.8, 1.5, step=0.2), ylim=(0.7, 1.5))
#ax2.grid()

ax3.set(ylabel='amplitude',
        title='speech stimulus waveform', xlabel='time (s)',
        xticks=np.arange(250, 275, step=5))
for channel in channels:
    ax3.plot(Time[t1:t2],channel[t1:t2])

fig.savefig('/media/cbru/SMEDY/results/example_envelopes/beta_envelopes.png')
fig.savefig('/media/cbru/SMEDY/results/example_envelopes/beta_envelopes.pdf')
plt.show()






